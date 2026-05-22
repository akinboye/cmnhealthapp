"""
Live Chat blueprint — user ↔ admin messaging
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models import db, User, ChatMessage
from datetime import datetime

live_chat_bp = Blueprint('live_chat', __name__)

# ── In-memory admin online status (set of admin user IDs) ──────────────────
_admin_online: set = set()


def _require_auth():
    """Return (user_id, None) on success, (None, error_response) on failure."""
    try:
        verify_jwt_in_request()
        return get_jwt_identity(), None
    except Exception:
        return None, (jsonify({'error': 'Authentication required'}), 401)


def _require_admin():
    """Return (user, None) on success, (None, error_response) on failure."""
    user_id, err = _require_auth()
    if err:
        return None, err
    user = User.query.get(user_id)
    if not user or not user.isAdmin:
        return None, (jsonify({'error': 'Admin access required'}), 403)
    return user, None


# ── Public: is any admin online? ───────────────────────────────────────────
@live_chat_bp.route('/api/livechat/status', methods=['GET'])
def admin_status():
    return jsonify({'online': len(_admin_online) > 0}), 200


# ── User: send a message ───────────────────────────────────────────────────
@live_chat_bp.route('/api/livechat/send', methods=['POST'])
def send_message():
    user_id, err = _require_auth()
    if err:
        return err

    data = request.get_json(silent=True) or {}
    text = (data.get('message') or '').strip()
    if not text:
        return jsonify({'error': 'Message is required'}), 400
    if len(text) > 2000:
        return jsonify({'error': 'Message exceeds 2000 characters'}), 400

    msg = ChatMessage(userId=user_id, sender='user', message=text)
    db.session.add(msg)
    db.session.commit()
    return jsonify({'message': msg.to_dict()}), 201


# ── User: fetch their own conversation (optionally since a message id) ─────
@live_chat_bp.route('/api/livechat/messages', methods=['GET'])
def get_messages():
    user_id, err = _require_auth()
    if err:
        return err

    since = request.args.get('since', 0, type=int)
    msgs = (ChatMessage.query
            .filter(ChatMessage.userId == user_id, ChatMessage.id > since)
            .order_by(ChatMessage.createdAt.asc())
            .limit(200).all())

    # Mark incoming admin messages as read
    (ChatMessage.query
     .filter_by(userId=user_id, sender='admin', isRead=False)
     .update({'isRead': True}))
    db.session.commit()

    return jsonify({'messages': [m.to_dict() for m in msgs]}), 200


# ── Admin: set online / offline ─────────────────────────────────────────────
@live_chat_bp.route('/api/livechat/admin/online', methods=['POST'])
def set_admin_online():
    admin, err = _require_admin()
    if err:
        return err

    data = request.get_json(silent=True) or {}
    if data.get('online', True):
        _admin_online.add(admin.id)
    else:
        _admin_online.discard(admin.id)

    return jsonify({'online': len(_admin_online) > 0}), 200


# ── Admin: list all user sessions (latest msg + unread count) ───────────────
@live_chat_bp.route('/api/livechat/admin/sessions', methods=['GET'])
def admin_sessions():
    admin, err = _require_admin()
    if err:
        return err

    from sqlalchemy import func
    subq = (db.session.query(
                ChatMessage.userId,
                func.max(ChatMessage.id).label('last_id'))
            .group_by(ChatMessage.userId)
            .subquery())

    rows = (db.session.query(ChatMessage, User)
            .join(subq, ChatMessage.id == subq.c.last_id)
            .join(User, User.id == ChatMessage.userId)
            .order_by(ChatMessage.createdAt.desc())
            .all())

    result = []
    for msg, u in rows:
        unread = ChatMessage.query.filter_by(
            userId=u.id, sender='user', isRead=False).count()
        result.append({
            'userId':        u.id,
            'userName':      f"{u.firstName} {u.lastName}",
            'userEmail':     u.email,
            'lastMessage':   msg.message,
            'lastMessageAt': msg.createdAt.isoformat() if msg.createdAt else None,
            'lastSender':    msg.sender,
            'unread':        unread,
        })

    return jsonify({'sessions': result}), 200


# ── Admin: get full conversation for one user ───────────────────────────────
@live_chat_bp.route('/api/livechat/admin/session/<target_user_id>', methods=['GET'])
def admin_get_session(target_user_id):
    admin, err = _require_admin()
    if err:
        return err

    since = request.args.get('since', 0, type=int)
    msgs = (ChatMessage.query
            .filter(ChatMessage.userId == target_user_id, ChatMessage.id > since)
            .order_by(ChatMessage.createdAt.asc())
            .limit(200).all())

    # Mark this user's messages as read
    (ChatMessage.query
     .filter_by(userId=target_user_id, sender='user', isRead=False)
     .update({'isRead': True}))
    db.session.commit()

    target = User.query.get(target_user_id)
    return jsonify({
        'messages': [m.to_dict() for m in msgs],
        'userName': f"{target.firstName} {target.lastName}" if target else 'Unknown',
    }), 200


# ── Admin: reply to a user ──────────────────────────────────────────────────
@live_chat_bp.route('/api/livechat/admin/reply', methods=['POST'])
def admin_reply():
    admin, err = _require_admin()
    if err:
        return err

    data = request.get_json(silent=True) or {}
    target_id = (data.get('userId') or '').strip()
    text = (data.get('message') or '').strip()

    if not target_id or not text:
        return jsonify({'error': 'userId and message are required'}), 400
    if len(text) > 2000:
        return jsonify({'error': 'Message exceeds 2000 characters'}), 400
    if not User.query.get(target_id):
        return jsonify({'error': 'User not found'}), 404

    msg = ChatMessage(userId=target_id, sender='admin', message=text)
    db.session.add(msg)
    db.session.commit()
    return jsonify({'message': msg.to_dict()}), 201


# ── Admin: total unread count (for badge in sidebar) ───────────────────────
@live_chat_bp.route('/api/livechat/admin/unread', methods=['GET'])
def admin_unread():
    admin, err = _require_admin()
    if err:
        return err

    count = ChatMessage.query.filter_by(sender='user', isRead=False).count()
    return jsonify({'unread': count}), 200
