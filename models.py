from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role          = db.Column(db.String(20), default='analyst')  # admin, analyst, viewer
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'role': self.role}


class Call(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    call_sid      = db.Column(db.String(64), unique=True)
    direction     = db.Column(db.String(10))
    from_number   = db.Column(db.String(20))
    to_number     = db.Column(db.String(20))
    status        = db.Column(db.String(20), default='initiated')
    started_at    = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at      = db.Column(db.DateTime)
    risk_score    = db.Column(db.Integer, default=0)
    transcript    = db.Column(db.Text)
    recording_url = db.Column(db.String(300))
    persona_used  = db.Column(db.Text)

    turns    = db.relationship('ConversationTurn', backref='call', lazy=True)
    alerts   = db.relationship('Alert', backref='call', lazy=True)
    comments = db.relationship('Comment', backref='call', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'call_sid': self.call_sid,
            'direction': self.direction,
            'from_number': self.from_number,
            'to_number': self.to_number,
            'status': self.status,
            'risk_score': self.risk_score,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
        }


class ConversationTurn(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    call_id    = db.Column(db.Integer, db.ForeignKey('call.id'))
    speaker    = db.Column(db.String(10))   # 'scammer' or 'victim'
    text       = db.Column(db.Text)
    timestamp  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {'speaker': self.speaker, 'text': self.text,
                'timestamp': self.timestamp.isoformat()}


class Alert(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    call_id     = db.Column(db.Integer, db.ForeignKey('call.id'))
    severity    = db.Column(db.String(10))   # low, medium, high
    description = db.Column(db.Text)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {'id': self.id, 'call_id': self.call_id,
                'severity': self.severity, 'description': self.description,
                'detected_at': self.detected_at.isoformat()}


class Comment(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    call_id    = db.Column(db.Integer, db.ForeignKey('call.id'))
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'))
    text       = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user       = db.relationship('User', backref='comments')

    def to_dict(self):
        return {'id': self.id, 'user': self.user.username if self.user else 'unknown',
                'text': self.text, 'created_at': self.created_at.isoformat()}


class DashboardSettings(db.Model):
    """Persisted per-user dashboard customization."""
    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    primary_color   = db.Column(db.String(20), default='#0d6efd')
    accent_color    = db.Column(db.String(20), default='#198754')
    bg_color        = db.Column(db.String(20), default='#121212')
    card_color      = db.Column(db.String(20), default='#1e1e2e')
    text_color      = db.Column(db.String(20), default='#e0e0e0')
    dashboard_title = db.Column(db.String(100), default='FraudSim Lab')
    logo_text       = db.Column(db.String(20), default='FSL')
    user            = db.relationship('User', backref=db.backref('settings', uselist=False))
