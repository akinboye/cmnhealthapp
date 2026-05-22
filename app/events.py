"""
Events blueprint — CRUD API for events
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models import db, Event, User
from datetime import datetime
from uuid import uuid4

events_bp = Blueprint('events', __name__)


def _require_admin():
    verify_jwt_in_request()
    uid = get_jwt_identity()
    user = User.query.get(uid)
    if not user or not user.isAdmin:
        return None, jsonify({'error': 'Admin access required'}), 403
    return user, None, None


# ── Public: list published events ────────────────────────────────────────────
@events_bp.route('/api/events/', methods=['GET'])
def list_events():
    events = Event.query.filter_by(isPublished=True).order_by(Event.eventDate.asc()).all()
    return jsonify({'events': [e.to_dict() for e in events]}), 200


# ── Admin: list all events (published + drafts) ───────────────────────────────
@events_bp.route('/api/events/all', methods=['GET'])
def list_all_events():
    try:
        verify_jwt_in_request()
        uid = get_jwt_identity()
        user = User.query.get(uid)
        if not user or not user.isAdmin:
            return jsonify({'error': 'Admin access required'}), 403
    except Exception:
        return jsonify({'error': 'Authentication required'}), 401

    events = Event.query.order_by(Event.eventDate.asc()).all()
    return jsonify({'events': [e.to_dict() for e in events]}), 200


# ── Admin: create event ───────────────────────────────────────────────────────
@events_bp.route('/api/events/', methods=['POST'])
def create_event():
    try:
        verify_jwt_in_request()
        uid = get_jwt_identity()
        user = User.query.get(uid)
        if not user or not user.isAdmin:
            return jsonify({'error': 'Admin access required'}), 403
    except Exception:
        return jsonify({'error': 'Authentication required'}), 401

    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    event_date_str = data.get('eventDate', '')
    if not event_date_str:
        return jsonify({'error': 'Event date is required'}), 400
    try:
        event_date = datetime.fromisoformat(event_date_str.replace('Z', ''))
    except ValueError:
        return jsonify({'error': 'Invalid event date format'}), 400

    end_date = None
    if data.get('endDate'):
        try:
            end_date = datetime.fromisoformat(data['endDate'].replace('Z', ''))
        except ValueError:
            pass

    event = Event(
        id=str(uuid4()),
        title=title,
        description=data.get('description', ''),
        location=data.get('location', ''),
        eventDate=event_date,
        endDate=end_date,
        organizer=data.get('organizer', 'Cure My Nation'),
        category=data.get('category', 'General'),
        imageBase64=data.get('imageBase64'),
        registrationUrl=data.get('registrationUrl', ''),
        isPublished=bool(data.get('isPublished', False)),
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'event': event.to_dict(), 'message': 'Event created'}), 201


# ── Admin: update event ───────────────────────────────────────────────────────
@events_bp.route('/api/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    try:
        verify_jwt_in_request()
        uid = get_jwt_identity()
        user = User.query.get(uid)
        if not user or not user.isAdmin:
            return jsonify({'error': 'Admin access required'}), 403
    except Exception:
        return jsonify({'error': 'Authentication required'}), 401

    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    data = request.get_json() or {}
    if 'title' in data:
        event.title = data['title'].strip()
    if 'description' in data:
        event.description = data['description']
    if 'location' in data:
        event.location = data['location']
    if 'organizer' in data:
        event.organizer = data['organizer']
    if 'category' in data:
        event.category = data['category']
    if 'registrationUrl' in data:
        event.registrationUrl = data['registrationUrl']
    if 'isPublished' in data:
        event.isPublished = bool(data['isPublished'])
    if 'imageBase64' in data:
        event.imageBase64 = data['imageBase64']
    if data.get('eventDate'):
        try:
            event.eventDate = datetime.fromisoformat(data['eventDate'].replace('Z', ''))
        except ValueError:
            pass
    if data.get('endDate'):
        try:
            event.endDate = datetime.fromisoformat(data['endDate'].replace('Z', ''))
        except ValueError:
            pass
    event.updatedAt = datetime.utcnow()
    db.session.commit()
    return jsonify({'event': event.to_dict(), 'message': 'Event updated'}), 200


# ── Admin: delete event ───────────────────────────────────────────────────────
@events_bp.route('/api/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        verify_jwt_in_request()
        uid = get_jwt_identity()
        user = User.query.get(uid)
        if not user or not user.isAdmin:
            return jsonify({'error': 'Admin access required'}), 403
    except Exception:
        return jsonify({'error': 'Authentication required'}), 401

    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted'}), 200
