"""
NAGARAM — Notification Service
Business logic for the notification system.
"""
from app.extensions import db
from app.models.notification import Notification


def create_notification(user_id, title, message, notification_type='info', link=None):
    """Create an in-app notification."""
    notif = Notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type,
        link=link,
    )
    db.session.add(notif)
    db.session.commit()
    return notif


def get_unread_count(user_id):
    """Get count of unread notifications for a user."""
    return Notification.query.filter_by(
        user_id=user_id, is_read=False
    ).count()


def get_user_notifications(user_id, limit=20, unread_only=False):
    """Get notifications for a user."""
    query = Notification.query.filter_by(user_id=user_id)
    if unread_only:
        query = query.filter_by(is_read=False)
    return query.order_by(Notification.created_at.desc()).limit(limit).all()


def mark_as_read(notification_id, user_id):
    """Mark a notification as read."""
    notif = Notification.query.filter_by(
        id=notification_id, user_id=user_id
    ).first()
    if notif:
        notif.is_read = True
        db.session.commit()
    return notif


def mark_all_as_read(user_id):
    """Mark all notifications as read for a user."""
    Notification.query.filter_by(
        user_id=user_id, is_read=False
    ).update({'is_read': True})
    db.session.commit()
