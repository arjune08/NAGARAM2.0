"""
NAGARAM — Notification Model
In-app notification system.
"""
from datetime import datetime, timezone
from app.extensions import db


class Notification(db.Model):
    """In-app notifications for users."""
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(30), default='info')
    # info, success, warning, alert, assignment, status_change, resolution
    link = db.Column(db.String(500))  # URL to related resource
    is_read = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )

    def __repr__(self):
        return f'<Notification user={self.user_id} "{self.title[:30]}">'
