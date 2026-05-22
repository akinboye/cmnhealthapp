"""
Violations Management APIs
"""

from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Violation, User, ViolationStatus, ViolationPriority, AuditLog
from datetime import datetime
from uuid import uuid4
from sqlalchemy import and_, or_
import json

violations_bp = Blueprint('violations', __name__, url_prefix='/api/violations')

_ALLOWED_TYPES = [
    'Medical Malpractice', 'Denial of Treatment', 'Negligence',
    'Over Charging', 'Infection Control', 'Privacy Violation',
    'Mistreated', 'Other',
]
_ALLOWED_PRIORITIES = ['low', 'medium', 'high', 'critical']
_ALLOWED_STATUSES = ['reported', 'inProgress', 'resolved', 'onhold', 'closed']
_MAX_HOSPITAL = 200
_MAX_DESC = 5000
_MAX_RESOLUTION = 2000


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


@violations_bp.route('/create', methods=['POST'])
@jwt_required()
def create_violation():
    """Create a new violation report"""
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        data = request.get_json(silent=True) or {}

        # Validate required fields
        required_fields = ['type', 'dateOfIncident', 'hospitalName', 'description', 'priority']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'{field} is required'}), 400

        vtype = str(data['type']).strip()
        if vtype not in _ALLOWED_TYPES:
            return jsonify({'success': False, 'message': 'Invalid violation type'}), 400

        priority = str(data.get('priority', 'medium')).strip().lower()
        if priority not in _ALLOWED_PRIORITIES:
            return jsonify({'success': False, 'message': 'Invalid priority value'}), 400

        hospital = str(data.get('hospitalName', '')).strip()[:_MAX_HOSPITAL]
        description = str(data.get('description', '')).strip()[:_MAX_DESC]
        
        # Create violation ID
        violation_id = f"VIOL_{user_id}_{datetime.utcnow().timestamp()}_{uuid4().hex[:8]}"
        
        # Parse date
        try:
            date_of_incident = datetime.fromisoformat(data['dateOfIncident'].replace('Z', '+00:00'))
        except:
            return jsonify({'success': False, 'message': 'Invalid date format'}), 400
        
        # Create violation
        violation = Violation(
            id=violation_id,
            userId=user_id,
            type=vtype,
            dateOfIncident=date_of_incident,
            hospitalName=hospital,
            description=description,
            priority=priority,
            status=ViolationStatus.REPORTED.value,
            state=str(data.get('state', user.state or '')).strip()[:100],
        )
        violation.set_evidence(data.get('evidence', []))
        
        db.session.add(violation)
        db.session.commit()
        
        # Log action
        log_action(user_id, 'VIOLATION_CREATED', 'violation', violation_id, {
            'type': vtype,
            'hospital': hospital[:50],
        })
        
        return jsonify({
            'success': True,
            'message': 'Violation reported successfully',
            'violation': violation.to_dict(),
        }), 201
        
    except Exception as e:
        print(f'\u274c Error creating violation: {e}')
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to create violation report'}), 500


@violations_bp.route('/my-violations', methods=['GET'])
@jwt_required()
def get_my_violations():
    """Get current user's violations"""
    try:
        user_id = get_jwt_identity()
        
        # Query user's violations
        violations = Violation.query.filter_by(userId=user_id).all()
        
        return jsonify({
            'success': True,
            'violations': [v.to_dict() for v in violations],
            'count': len(violations),
        }), 200
        
    except Exception as e:
        print(f'\u274c Error getting user violations: {e}')
        return jsonify({'success': False, 'message': 'Failed to retrieve violations'}), 500


@violations_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_violations():
    """Get all violations (admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        
        if not user or not user.isAdmin:
            return jsonify({'success': False, 'message': 'Admin access required'}), 403
        
        # Get all violations with reporter info
        violations = Violation.query.order_by(Violation.dateReported.desc()).all()
        violations_data = []
        for v in violations:
            v_dict = v.to_dict()
            reporter = User.query.filter_by(id=v.userId).first()
            if reporter:
                v_dict['reporter'] = {
                    'id': reporter.id,
                    'firstName': reporter.firstName,
                    'lastName': reporter.lastName,
                    'email': reporter.email,
                    'phone': reporter.phone or '',
                    'state': reporter.state or '',
                }
            violations_data.append(v_dict)
        
        return jsonify({
            'success': True,
            'violations': violations_data,
            'count': len(violations_data),
        }), 200
        
    except Exception as e:
        print(f'\u274c Error getting all violations: {e}')
        return jsonify({'success': False, 'message': 'Failed to retrieve violations'}), 500


@violations_bp.route('/<violation_id>', methods=['GET'])
@jwt_required()
def get_violation(violation_id):
    """Get a specific violation"""
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        
        violation = Violation.query.filter_by(id=violation_id).first()
        
        if not violation:
            return jsonify({'success': False, 'message': 'Violation not found'}), 404
        
        # Check permissions: user can view own, admin can view all
        if violation.userId != user_id and not user.isAdmin:
            return jsonify({'success': False, 'message': 'Access denied'}), 403
        
        # Get reporter info if admin
        reporter = None
        if user.isAdmin:
            reporter_user = User.query.filter_by(id=violation.userId).first()
            if reporter_user:
                reporter = {
                    'id': reporter_user.id,
                    'name': f"{reporter_user.firstName} {reporter_user.lastName}",
                    'email': reporter_user.email,
                    'phone': reporter_user.phone,
                    'state': reporter_user.state,
                }
        
        return jsonify({
            'success': True,
            'violation': violation.to_dict(),
            'reporter': reporter,
        }), 200
        
    except Exception as e:
        print(f'\u274c Error getting violation: {e}')
        return jsonify({'success': False, 'message': 'Failed to retrieve violation'}), 500


@violations_bp.route('/<violation_id>/update-status', methods=['PUT'])
@jwt_required()
def update_violation_status(violation_id):
    """Update violation status (admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        
        if not user or not user.isAdmin:
            return jsonify({'success': False, 'message': 'Admin access required'}), 403
        
        violation = Violation.query.filter_by(id=violation_id).first()
        
        if not violation:
            return jsonify({'success': False, 'message': 'Violation not found'}), 404
        
        data = request.get_json(silent=True) or {}
        new_status = str(data.get('status', '')).strip()
        resolution = str(data.get('resolution', '')).strip()[:_MAX_RESOLUTION]
        
        if not new_status or new_status not in _ALLOWED_STATUSES:
            return jsonify({'success': False, 'message': 'Invalid status'}), 400
        
        # Update violation
        violation.status = new_status
        if new_status == ViolationStatus.RESOLVED.value:
            violation.dateResolved = datetime.utcnow()
            violation.resolution = resolution
        
        violation.updatedAt = datetime.utcnow()
        db.session.commit()
        
        # Log action
        log_action(user_id, 'VIOLATION_STATUS_UPDATED', 'violation', violation_id, {
            'newStatus': new_status,
            'resolution': resolution[:100] if resolution else None,
        })
        
        return jsonify({
            'success': True,
            'message': 'Violation status updated',
            'violation': violation.to_dict(),
        }), 200
        
    except Exception as e:
        print(f'\u274c Error updating violation: {e}')
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to update violation status'}), 500


@violations_bp.route('/filter', methods=['POST'])
@jwt_required()
def filter_violations():
    """Filter violations by status, priority, type, etc."""
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        
        if not user or not user.isAdmin:
            return jsonify({'success': False, 'message': 'Admin access required'}), 403
        
        data = request.get_json(silent=True) or {}
        query = Violation.query

        # Filter by status
        if data.get('status'):
            status = str(data['status']).strip()
            if status in _ALLOWED_STATUSES:
                query = query.filter_by(status=status)

        # Filter by priority
        if data.get('priority'):
            priority = str(data['priority']).strip().lower()
            if priority in _ALLOWED_PRIORITIES:
                query = query.filter_by(priority=priority)

        # Filter by type
        if data.get('type'):
            vtype = str(data['type']).strip()
            if vtype in _ALLOWED_TYPES:
                query = query.filter_by(type=vtype)

        # Filter by state
        if data.get('state'):
            query = query.filter_by(state=str(data['state']).strip()[:100])

        # Search in description or hospital name
        if data.get('search'):
            search_term = f"%{str(data['search'])[:100]}%"
            query = query.filter(
                or_(
                    Violation.description.ilike(search_term),
                    Violation.hospitalName.ilike(search_term),
                    Violation.type.ilike(search_term),
                )
            )
        
        violations = query.all()
        
        return jsonify({
            'success': True,
            'violations': [v.to_dict() for v in violations],
            'count': len(violations),
        }), 200
        
    except Exception as e:
        print(f'\u274c Error filtering violations: {e}')
        return jsonify({'success': False, 'message': 'Failed to filter violations'}), 500


@violations_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    """Get violation statistics"""
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        
        if user.isAdmin:
            # Admin gets global statistics
            total = Violation.query.count()
            reported = Violation.query.filter_by(status=ViolationStatus.REPORTED.value).count()
            in_progress = Violation.query.filter_by(status=ViolationStatus.IN_PROGRESS.value).count()
            resolved = Violation.query.filter_by(status=ViolationStatus.RESOLVED.value).count()
            on_hold = Violation.query.filter_by(status=ViolationStatus.ON_HOLD.value).count()
            critical = Violation.query.filter_by(priority=ViolationPriority.CRITICAL.value).count()
            high     = Violation.query.filter_by(priority=ViolationPriority.HIGH.value).count()
            medium   = Violation.query.filter_by(priority=ViolationPriority.MEDIUM.value).count()
            low      = Violation.query.filter_by(priority=ViolationPriority.LOW.value).count()
        else:
            # User gets personal statistics
            total = Violation.query.filter_by(userId=user_id).count()
            reported = Violation.query.filter_by(userId=user_id, status=ViolationStatus.REPORTED.value).count()
            in_progress = Violation.query.filter_by(userId=user_id, status=ViolationStatus.IN_PROGRESS.value).count()
            resolved = Violation.query.filter_by(userId=user_id, status=ViolationStatus.RESOLVED.value).count()
            on_hold = Violation.query.filter_by(userId=user_id, status=ViolationStatus.ON_HOLD.value).count()
            critical = Violation.query.filter_by(userId=user_id, priority=ViolationPriority.CRITICAL.value).count()
            high     = Violation.query.filter_by(userId=user_id, priority=ViolationPriority.HIGH.value).count()
            medium   = Violation.query.filter_by(userId=user_id, priority=ViolationPriority.MEDIUM.value).count()
            low      = Violation.query.filter_by(userId=user_id, priority=ViolationPriority.LOW.value).count()
        
        resolution_rate = (resolved / total * 100) if total > 0 else 0
        
        return jsonify({
            'success': True,
            'statistics': {
                'total': total,
                'reported': reported,
                'inProgress': in_progress,
                'resolved': resolved,
                'onHold': on_hold,
                'resolutionRate': round(resolution_rate, 2),
                'isAdmin': user.isAdmin,
                'byPriority': {
                    'critical': critical,
                    'high':     high,
                    'medium':   medium,
                    'low':      low,
                },
            },
        }), 200
        
    except Exception as e:
        print(f'\u274c Error getting statistics: {e}')
        return jsonify({'success': False, 'message': 'Failed to retrieve statistics'}), 500
