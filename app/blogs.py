"""
Blog Management APIs
"""

from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models import db, BlogPost, User, AuditLog
from datetime import datetime
from uuid import uuid4
import json

blogs_bp = Blueprint('blogs', __name__, url_prefix='/api/blogs')

_MAX_TITLE    = 300
_MAX_DESC     = 1000
_MAX_CATEGORY = 100


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


@blogs_bp.route('/', methods=['GET'])
def get_published_blogs():
    """Get all published blog posts (public)"""
    try:
        blogs = BlogPost.query.filter_by(isPublished=True).order_by(BlogPost.createdAt.desc()).all()
        return jsonify({
            'success': True,
            'blogs': [b.to_dict() for b in blogs],
            'count': len(blogs),
        }), 200
    except Exception as e:
        print(f'\u274c Error getting published blogs: {e}')
        return jsonify({'success': False, 'message': 'Failed to retrieve blogs'}), 500


@blogs_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_blogs():
    """Get all blog posts (admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if not user or not user.isAdmin:
            return jsonify({'success': False, 'message': 'Admin access required'}), 403

        blogs = BlogPost.query.order_by(BlogPost.createdAt.desc()).all()
        return jsonify({
            'success': True,
            'blogs': [b.to_dict() for b in blogs],
            'count': len(blogs),
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to retrieve blogs'}), 500


@blogs_bp.route('/<blog_id>', methods=['GET'])
def get_blog(blog_id):
    """Get a single blog post by ID"""
    try:
        blog = BlogPost.query.filter_by(id=blog_id).first()
        if not blog:
            return jsonify({'success': False, 'message': 'Blog post not found'}), 404
        # Only return unpublished blogs to admins
        if not blog.isPublished:
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                user = User.query.filter_by(id=user_id).first()
                if not user or not user.isAdmin:
                    return jsonify({'success': False, 'message': 'Blog post not found'}), 404
            except Exception:
                return jsonify({'success': False, 'message': 'Blog post not found'}), 404

        return jsonify({'success': True, 'blog': blog.to_dict()}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to retrieve blog post'}), 500


@blogs_bp.route('/', methods=['POST'])
@jwt_required()
def create_blog():
    """Create a new blog post (admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if not user or not user.isAdmin:
            return jsonify({'success': False, 'message': 'Admin access required'}), 403

        data = request.get_json(silent=True) or {}
        if not data.get('title') or not data.get('content'):
            return jsonify({'success': False, 'message': 'title and content are required'}), 400

        blog = BlogPost(
            id=str(uuid4()),
            title=str(data['title']).strip()[:_MAX_TITLE],
            description=str(data.get('description', '')).strip()[:_MAX_DESC],
            content=data['content'],
            imageBase64=data.get('imageBase64'),
            authorId=user_id,
            authorName=f"{user.firstName} {user.lastName}",
            category=str(data.get('category', 'General')).strip()[:_MAX_CATEGORY],
            isPublished=bool(data.get('isPublished', False)),
        )

        db.session.add(blog)
        db.session.commit()
        log_action(user_id, 'BLOG_CREATED', 'blog', blog.id, {'title': blog.title})

        return jsonify({
            'success': True,
            'message': 'Blog post created successfully',
            'blog': blog.to_dict(),
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to create blog post'}), 500


@blogs_bp.route('/<blog_id>', methods=['PUT'])
@jwt_required()
def update_blog(blog_id):
    """Update an existing blog post (admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if not user or not user.isAdmin:
            return jsonify({'success': False, 'message': 'Admin access required'}), 403

        blog = BlogPost.query.filter_by(id=blog_id).first()
        if not blog:
            return jsonify({'success': False, 'message': 'Blog post not found'}), 404

        data = request.get_json(silent=True) or {}
        if 'title' in data:
            blog.title = str(data['title']).strip()[:_MAX_TITLE]
        if 'description' in data:
            blog.description = str(data['description']).strip()[:_MAX_DESC]
        if 'content' in data:
            blog.content = data['content']
        if 'imageBase64' in data:
            blog.imageBase64 = data['imageBase64']
        if 'category' in data:
            blog.category = str(data['category']).strip()[:_MAX_CATEGORY]
        if 'isPublished' in data:
            blog.isPublished = bool(data['isPublished'])
        blog.updatedAt = datetime.utcnow()

        db.session.commit()
        log_action(user_id, 'BLOG_UPDATED', 'blog', blog_id)

        return jsonify({
            'success': True,
            'message': 'Blog post updated successfully',
            'blog': blog.to_dict(),
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to update blog post'}), 500


@blogs_bp.route('/<blog_id>', methods=['DELETE'])
@jwt_required()
def delete_blog(blog_id):
    """Delete a blog post (admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if not user or not user.isAdmin:
            return jsonify({'success': False, 'message': 'Admin access required'}), 403

        blog = BlogPost.query.filter_by(id=blog_id).first()
        if not blog:
            return jsonify({'success': False, 'message': 'Blog post not found'}), 404

        db.session.delete(blog)
        db.session.commit()
        log_action(user_id, 'BLOG_DELETED', 'blog', blog_id)

        return jsonify({'success': True, 'message': 'Blog post deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to delete blog post'}), 500


@blogs_bp.route('/<blog_id>/publish', methods=['PUT'])
@jwt_required()
def toggle_publish(blog_id):
    """Toggle blog post publish status (admin only)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        if not user or not user.isAdmin:
            return jsonify({'success': False, 'message': 'Admin access required'}), 403

        blog = BlogPost.query.filter_by(id=blog_id).first()
        if not blog:
            return jsonify({'success': False, 'message': 'Blog post not found'}), 404

        blog.isPublished = not blog.isPublished
        blog.updatedAt = datetime.utcnow()
        db.session.commit()
        log_action(user_id, 'BLOG_PUBLISH_TOGGLED', 'blog', blog_id, {'isPublished': blog.isPublished})

        return jsonify({
            'success': True,
            'message': f'Blog post {"published" if blog.isPublished else "unpublished"}',
            'blog': blog.to_dict(),
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to update blog post'}), 500
