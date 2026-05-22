"""
Database models — PostgreSQL (SQLAlchemy ORM)
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum
import bcrypt
import json

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)
    adminRole = db.Column(db.String(50), nullable=True)
    adminPrivileges = db.Column(db.Text, nullable=True)
    language = db.Column(db.String(10), default='en')
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    violations = db.relationship('Violation', backref='reporter', lazy=True, cascade='all, delete-orphan')
    blogs = db.relationship('BlogPost', backref='author_user', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def get_admin_privileges(self):
        if self.adminPrivileges:
            try:
                return json.loads(self.adminPrivileges)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    def set_admin_privileges(self, privileges):
        self.adminPrivileges = json.dumps(privileges) if privileges else None

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'username': self.username or (self.firstName.lower() + self.lastName.lower()),
            'phone': self.phone or '',
            'address': self.address or '',
            'state': self.state or '',
            'isAdmin': self.isAdmin,
            'adminRole': self.adminRole,
            'adminPrivileges': self.get_admin_privileges(),
            'language': self.language,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
        }


class ViolationType(str, Enum):
    MEDICAL_MALPRACTICE = "Medical Malpractice"
    DENIAL_OF_TREATMENT = "Denial of Treatment"
    NEGLIGENCE = "Negligence"
    OVER_CHARGING = "Over Charging"
    INFECTION_CONTROL = "Infection Control"
    PRIVACY_VIOLATION = "Privacy Violation"
    MISTREATED = "Mistreated"
    OTHER = "Other"


class ViolationStatus(str, Enum):
    REPORTED = "reported"
    IN_PROGRESS = "inProgress"
    RESOLVED = "resolved"
    ON_HOLD = "onhold"


class ViolationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Violation(db.Model):
    __tablename__ = 'violations'

    id = db.Column(db.String(100), primary_key=True)
    userId = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    type = db.Column(db.String(50), nullable=False)
    dateOfIncident = db.Column(db.DateTime, nullable=False)
    hospitalName = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    evidence = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), nullable=False, default='medium')
    status = db.Column(db.String(20), nullable=False, default='reported')
    dateReported = db.Column(db.DateTime, default=datetime.utcnow)
    dateResolved = db.Column(db.DateTime, nullable=True)
    resolution = db.Column(db.Text, nullable=True)
    state = db.Column(db.String(100), nullable=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_evidence(self):
        if self.evidence:
            try:
                return json.loads(self.evidence)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    def set_evidence(self, evidence_list):
        self.evidence = json.dumps(evidence_list) if evidence_list else '[]'

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'type': self.type,
            'dateOfIncident': self.dateOfIncident.isoformat() if self.dateOfIncident else None,
            'hospitalName': self.hospitalName,
            'description': self.description,
            'evidence': self.get_evidence(),
            'priority': self.priority,
            'status': self.status,
            'dateReported': self.dateReported.isoformat() if self.dateReported else None,
            'dateResolved': self.dateResolved.isoformat() if self.dateResolved else None,
            'resolution': self.resolution,
            'state': self.state,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
        }


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(200), nullable=False)
    entity = db.Column(db.String(100), nullable=False)
    entityId = db.Column(db.String(100), nullable=True)
    details = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    ipAddress = db.Column(db.String(50), nullable=True)


class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'

    id = db.Column(db.String(36), primary_key=True)
    userId = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    token = db.Column(db.String(64), unique=True, nullable=False, index=True)
    expiresAt = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)


class BlogPost(db.Model):
    __tablename__ = 'blog_posts'

    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    content = db.Column(db.Text, nullable=False)
    imageBase64 = db.Column(db.Text, nullable=True)
    authorId = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    authorName = db.Column(db.String(200), nullable=False, default='Admin')
    category = db.Column(db.String(100), nullable=True)
    isPublished = db.Column(db.Boolean, default=False, index=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description or '',
            'content': self.content,
            'imageBase64': self.imageBase64,
            'author': self.authorName,
            'authorId': self.authorId,
            'category': self.category or 'General',
            'isPublished': self.isPublished,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
            'updatedAt': self.updatedAt.isoformat() if self.updatedAt else None,
        }


def init_db(app):
    with app.app_context():
        db.create_all()
        print('[OK] Database initialized')


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(300), nullable=True)
    eventDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=True)
    organizer = db.Column(db.String(200), nullable=True, default='Cure My Nation')
    category = db.Column(db.String(100), nullable=True, default='General')
    imageBase64 = db.Column(db.Text, nullable=True)
    registrationUrl = db.Column(db.String(500), nullable=True)
    isPublished = db.Column(db.Boolean, default=False, index=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description or '',
            'location': self.location or '',
            'eventDate': self.eventDate.isoformat() if self.eventDate else None,
            'endDate': self.endDate.isoformat() if self.endDate else None,
            'organizer': self.organizer or 'Cure My Nation',
            'category': self.category or 'General',
            'imageBase64': self.imageBase64,
            'registrationUrl': self.registrationUrl or '',
            'isPublished': self.isPublished,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
        }


class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId    = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    sender    = db.Column(db.String(10), nullable=False)   # 'user' | 'admin'
    message   = db.Column(db.Text, nullable=False)
    isRead    = db.Column(db.Boolean, default=False, index=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            'id':        self.id,
            'userId':    self.userId,
            'sender':    self.sender,
            'message':   self.message,
            'isRead':    self.isRead,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
        }
