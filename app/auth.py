"""
Authentication and User Management APIs
"""

from flask import request, jsonify, Blueprint, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_mail import Mail, Message
from models import db, User, AuditLog, PasswordResetToken
from datetime import datetime, timedelta
from uuid import uuid4
import re
import json
import secrets

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Field length constants
_MAX_EMAIL    = 254
_MAX_NAME     = 100
_MAX_PHONE    = 30
_MAX_ADDRESS  = 300
_MAX_PASSWORD = 128
_MAX_STATE    = 100


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password: str):
    """Require ≥8 chars, at least one letter and one digit."""
    if len(password) < 8:
        return False, 'Password must be at least 8 characters'
    if not re.search(r'[A-Za-z]', password):
        return False, 'Password must contain at least one letter'
    if not re.search(r'[0-9]', password):
        return False, 'Password must contain at least one number'
    return True, 'Valid'


def log_action(user_id, action, entity, entity_id=None, details=None):
    """Log user action for audit trail"""
    try:
        log = AuditLog(
            userId=user_id,
            action=action,
            entity=entity,
            entityId=entity_id,
            details=json.dumps(details) if details else None,
            ipAddress=request.remote_addr,
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"❌ Error logging action: {e}")


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json(silent=True) or {}

        # Validate required fields
        required_fields = ['email', 'firstName', 'lastName', 'password', 'state']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} is required'}), 400

        email     = data['email'].strip().lower()[:_MAX_EMAIL]
        firstName = data['firstName'].strip()[:_MAX_NAME]
        lastName  = data['lastName'].strip()[:_MAX_NAME]
        password  = data['password']  # do NOT strip passwords
        state     = data['state'].strip()[:_MAX_STATE]
        phone     = (data.get('phone') or '').strip()[:_MAX_PHONE]
        address   = (data.get('address') or '').strip()[:_MAX_ADDRESS]

        # Length guards
        if len(email) > _MAX_EMAIL:
            return jsonify({'success': False, 'message': 'Email too long'}), 400
        if len(password) > _MAX_PASSWORD:
            return jsonify({'success': False, 'message': 'Password too long'}), 400
        if not firstName or not lastName:
            return jsonify({'success': False, 'message': 'Name fields cannot be blank after trimming'}), 400

        # Validate email format
        if not validate_email(email):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already registered'}), 409

        # Validate password
        valid, msg = validate_password(password)
        if not valid:
            return jsonify({'success': False, 'message': msg}), 400

        # Create new user
        user = User(
            id=str(uuid4()),
            email=email,
            firstName=firstName,
            lastName=lastName,
            phone=phone,
            address=address,
            state=state,
            username=(data.get('username') or '').strip()[:_MAX_NAME] or None,
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        log_action(user.id, 'USER_REGISTERED', 'user', user.id)

        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(days=30)
        )

        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'token': access_token,
            'user': user.to_dict(),
        }), 201

    except Exception as e:
        print(f'\u274c Error in register: {e}')
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Registration failed. Please try again.'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json(silent=True) or {}

        email    = (data.get('email') or '').strip().lower()[:_MAX_EMAIL]
        password = (data.get('password') or '')

        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password required'}), 400

        # Constant-time lookup to prevent user enumeration via timing
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            log_action(None, 'LOGIN_FAILED', 'auth', details={'email': email})
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(days=30)
        )

        log_action(user.id, 'LOGIN_SUCCESS', 'auth', user.id)

        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': access_token,
            'user': user.to_dict(),
        }), 200

    except Exception as e:
        print(f'\u274c Error in login: {e}')
        return jsonify({'success': False, 'message': 'Login failed. Please try again.'}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'user': user.to_dict(),
        }), 200
        
    except Exception as e:
        print(f'\u274c Error getting current user: {e}')
        return jsonify({'success': False, 'message': 'Could not retrieve user'}), 500


@auth_bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        data = request.get_json(silent=True) or {}

        # Update allowed fields with length guards
        if 'firstName' in data:
            user.firstName = str(data['firstName']).strip()[:_MAX_NAME]
        if 'lastName' in data:
            user.lastName = str(data['lastName']).strip()[:_MAX_NAME]
        if 'phone' in data:
            user.phone = str(data['phone']).strip()[:_MAX_PHONE]
        if 'state' in data:
            user.state = str(data['state']).strip()[:_MAX_STATE]
        if 'address' in data:
            user.address = str(data['address']).strip()[:_MAX_ADDRESS]
        if 'language' in data:
            user.language = str(data['language']).strip()[:20]
        if 'preferredLanguage' in data:
            user.language = str(data['preferredLanguage']).strip()[:20]
        
        user.updatedAt = datetime.utcnow()
        db.session.commit()
        
        # Log action
        log_action(user_id, 'PROFILE_UPDATED', 'user', user_id)
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': user.to_dict(),
        }), 200
        
    except Exception as e:
        print(f'\u274c Error updating profile: {e}')
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Profile update failed'}), 500


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        data = request.get_json(silent=True) or {}
        old_password = data.get('oldPassword', '')
        new_password = data.get('newPassword', '')

        if not old_password or not new_password:
            return jsonify({'success': False, 'message': 'Both passwords are required'}), 400
        if len(new_password) > _MAX_PASSWORD:
            return jsonify({'success': False, 'message': 'New password too long'}), 400
        
        # Verify old password
        if not user.check_password(old_password):
            return jsonify({'success': False, 'message': 'Current password is incorrect'}), 401
        
        # Validate new password
        valid, msg = validate_password(new_password)
        if not valid:
            return jsonify({'success': False, 'message': msg}), 400
        
        # Set new password
        user.set_password(new_password)
        user.updatedAt = datetime.utcnow()
        db.session.commit()
        
        # Log action
        log_action(user_id, 'PASSWORD_CHANGED', 'user', user_id)
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully',
        }), 200
        
    except Exception as e:
        print(f'\u274c Error changing password: {e}')
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Password change failed'}), 500


@auth_bp.route('/verify-token', methods=['POST'])
@jwt_required()
def verify_token():
    """Verify if token is still valid"""
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Token is valid',
            'user': user.to_dict(),
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Invalid token'}), 401


@auth_bp.route('/delete-account', methods=['DELETE'])
@jwt_required()
def delete_account():
    """Delete current user's account"""
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Account deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Account deletion failed'}), 500


@auth_bp.route('/stats', methods=['GET'])
def public_stats():
    """Public stats for landing page (no auth required)"""
    try:
        count = User.query.count()
        return jsonify({'success': True, 'userCount': count}), 200
    except Exception:
        return jsonify({'success': True, 'userCount': 0}), 200


@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    """Get all users (admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        
        if not user or not user.isAdmin:
            return jsonify({'success': False, 'message': 'Admin access required'}), 403
        
        users = User.query.all()
        return jsonify({
            'success': True,
            'users': [u.to_dict() for u in users],
            'count': len(users),
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Could not retrieve users'}), 500
@jwt_required()
def create_admin():
    """Create admin account (superAdmin only)"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.filter_by(id=user_id).first()
        
        if not current_user or current_user.adminRole != 'superAdmin':
            return jsonify({'success': False, 'message': 'Only SuperAdmin can create admin accounts'}), 403
        
        data = request.get_json()
        required = ['email', 'password', 'firstName', 'lastName']
        for field in required:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} is required'}), 400
        
        email = data['email'].strip().lower()[:_MAX_EMAIL]
        if not validate_email(email):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already registered'}), 409

        valid, msg = validate_password(data['password'])
        if not valid:
            return jsonify({'success': False, 'message': msg}), 400

        new_admin = User(
            id=str(uuid4()),
            email=email,
            firstName=str(data['firstName']).strip()[:_MAX_NAME],
            lastName=str(data['lastName']).strip()[:_MAX_NAME],
            phone=str(data.get('phone', '')).strip()[:_MAX_PHONE],
            state=str(data.get('state', '')).strip()[:_MAX_STATE],
            isAdmin=True,
            adminRole=data.get('adminRole', 'admin'),
        )
        new_admin.set_password(data['password'])
        new_admin.set_admin_privileges(data.get('adminPrivileges', []))
        
        db.session.add(new_admin)
        db.session.commit()
        
        log_action(user_id, 'ADMIN_CREATED', 'user', new_admin.id, {'email': email})
        
        return jsonify({
            'success': True,
            'message': 'Admin account created successfully',
            'user': new_admin.to_dict(),
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to create admin account'}), 500


@auth_bp.route('/update-admin', methods=['PUT'])
@jwt_required()
def update_admin():
    """Update admin role and privileges (superAdmin only)"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.filter_by(id=user_id).first()
        
        if not current_user or current_user.adminRole != 'superAdmin':
            return jsonify({'success': False, 'message': 'Only SuperAdmin can update admin roles'}), 403
        
        data = request.get_json(silent=True) or {}
        email = (data.get('email') or '').strip().lower()[:_MAX_EMAIL]
        
        target = User.query.filter_by(email=email).first()
        if not target:
            return jsonify({'success': False, 'message': 'Admin account not found'}), 404
        
        # Prevent changing own role away from superAdmin
        if target.id == user_id and data.get('adminRole') != 'superAdmin':
            return jsonify({'success': False, 'message': 'Cannot change your own role'}), 400
        
        if 'adminRole' in data:
            target.adminRole = data['adminRole']
        if 'adminPrivileges' in data:
            target.set_admin_privileges(data['adminPrivileges'])
        
        db.session.commit()
        log_action(user_id, 'ADMIN_UPDATED', 'user', target.id)
        
        return jsonify({'success': True, 'message': 'Admin updated', 'user': target.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to update admin'}), 500


@auth_bp.route('/users/<target_user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(target_user_id):
    """Delete a user account (superAdmin only)"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.filter_by(id=user_id).first()
        
        if not current_user or current_user.adminRole != 'superAdmin':
            return jsonify({'success': False, 'message': 'Only SuperAdmin can delete accounts'}), 403
        
        if target_user_id == user_id:
            return jsonify({'success': False, 'message': 'Cannot delete your own account'}), 400
        
        target = User.query.filter_by(id=target_user_id).first()
        if not target:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        db.session.delete(target)
        db.session.commit()
        log_action(user_id, 'USER_DELETED', 'user', target_user_id)
        
        return jsonify({'success': True, 'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to delete user'}), 500


@auth_bp.route('/users/<target_user_id>/change-role', methods=['PUT'])
@jwt_required()
def change_user_role(target_user_id):
    """Change a user's role (superAdmin only)"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.filter_by(id=user_id).first()

        if not current_user or current_user.adminRole != 'superAdmin':
            return jsonify({'success': False, 'message': 'Only SuperAdmin can change roles'}), 403

        target = User.query.filter_by(id=target_user_id).first()
        if not target:
            return jsonify({'success': False, 'message': 'User not found'}), 404

        if target.id == user_id:
            return jsonify({'success': False, 'message': 'Cannot change your own role'}), 400

        data = request.get_json(silent=True) or {}
        new_role = str(data.get('role', '')).strip()

        if new_role not in ('user', 'admin', 'superAdmin'):
            return jsonify({'success': False, 'message': 'Invalid role. Must be user, admin, or superAdmin'}), 400

        if new_role == 'user':
            target.isAdmin = False
            target.adminRole = None
        elif new_role == 'admin':
            target.isAdmin = True
            target.adminRole = 'admin'
        elif new_role == 'superAdmin':
            target.isAdmin = True
            target.adminRole = 'superAdmin'

        db.session.commit()
        log_action(user_id, 'USER_ROLE_CHANGED', 'user', target_user_id, {'newRole': new_role})

        return jsonify({
            'success': True,
            'message': f'Role updated to {new_role}',
            'user': target.to_dict(),
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to change role'}), 500


# ──────────────────────────────────────────────────────────────
#  Password Reset
# ──────────────────────────────────────────────────────────────

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Send password-reset link to user's email"""
    try:
        data = request.get_json(silent=True) or {}
        email = str(data.get('email', '')).strip().lower()[:_MAX_EMAIL]

        if not email or not validate_email(email):
            return jsonify({'success': False, 'message': 'Valid email address required'}), 400

        # Always return the same response to prevent email enumeration
        generic_ok = jsonify({
            'success': True,
            'message': 'If that email is registered you will receive a reset link shortly.',
        }), 200

        user = User.query.filter_by(email=email).first()
        if not user:
            return generic_ok

        # Invalidate any existing unused tokens for this user
        PasswordResetToken.query.filter_by(userId=user.id, used=False).update({'used': True})
        db.session.flush()

        # Create new token (64 hex chars = 256 bits of entropy)
        token = secrets.token_hex(32)
        reset_token = PasswordResetToken(
            id=str(uuid4()),
            userId=user.id,
            token=token,
            expiresAt=datetime.utcnow() + timedelta(minutes=10),
        )
        db.session.add(reset_token)
        db.session.commit()

        app_url = current_app.config.get('APP_URL', 'http://localhost:5000')
        reset_url = f'{app_url}/reset-password?token={token}'

        mail = Mail(current_app)
        msg = Message(
            subject='Reset your Cure My Nation password',
            recipients=[user.email],
        )
        msg.body = (
            f'Hi {user.firstName},\n\n'
            f'You requested a password reset for your Cure My Nation account.\n\n'
            f'Click the link below to set a new password. This link expires in 10 minutes.\n\n'
            f'{reset_url}\n\n'
            f'If you did not request this, please ignore this email — your password will not change.\n\n'
            f'— Cure My Nation Team'
        )
        msg.html = (
            f'<p>Hi <strong>{user.firstName}</strong>,</p>'
            f'<p>You requested a password reset for your Cure My Nation account.</p>'
            f'<p><a href="{reset_url}" style="background:#1E3A8A;color:#fff;padding:10px 20px;'
            f'border-radius:8px;text-decoration:none;font-weight:bold;">Reset Password</a></p>'
            f'<p style="color:#888;font-size:12px;">This link expires in <strong>10 minutes</strong>. '
            f'If you did not request this, ignore this email.</p>'
            f'<p style="color:#888;font-size:12px;">Or copy this link: {reset_url}</p>'
        )
        mail.send(msg)
        log_action(user.id, 'PASSWORD_RESET_REQUESTED', 'auth', user.id)
        return generic_ok

    except Exception as e:
        print(f'\u274c Error in forgot_password: {e}')
        db.session.rollback()
        # Still return generic success to prevent email enumeration
        return jsonify({
            'success': True,
            'message': 'If that email is registered you will receive a reset link shortly.',
        }), 200


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password using a valid token"""
    try:
        data = request.get_json(silent=True) or {}
        token = str(data.get('token', '')).strip()
        new_password = str(data.get('password', '')).strip()

        if not token or not new_password:
            return jsonify({'success': False, 'message': 'Token and new password are required'}), 400

        if len(new_password) > _MAX_PASSWORD:
            return jsonify({'success': False, 'message': 'Password too long'}), 400

        valid, msg = validate_password(new_password)
        if not valid:
            return jsonify({'success': False, 'message': msg}), 400

        reset_token = PasswordResetToken.query.filter_by(token=token, used=False).first()

        if not reset_token:
            return jsonify({'success': False, 'message': 'Invalid or expired reset link'}), 400

        if datetime.utcnow() > reset_token.expiresAt:
            reset_token.used = True
            db.session.commit()
            return jsonify({'success': False, 'message': 'Reset link has expired. Please request a new one'}), 400

        user = User.query.filter_by(id=reset_token.userId).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404

        user.set_password(new_password)
        user.updatedAt = datetime.utcnow()
        reset_token.used = True
        db.session.commit()

        log_action(user.id, 'PASSWORD_RESET_COMPLETED', 'auth', user.id)
        return jsonify({'success': True, 'message': 'Password reset successfully. You can now log in.'}), 200

    except Exception as e:
        print(f'\u274c Error in reset_password: {e}')
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Password reset failed. Please try again.'}), 500
