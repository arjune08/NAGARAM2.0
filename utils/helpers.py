"""
NAGARAM — Utility Helpers
Common utility functions used across the application.
"""
import os
import uuid
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
from flask import current_app


def generate_issue_id(issue_type='civic'):
    """Generate a unique issue ID. Format: NG-XXXX or AG-XXXX."""
    from app.models.issue import Issue
    prefix = 'NG' if issue_type == 'civic' else 'AG'
    # Get the latest issue number for this type
    latest = Issue.query.filter(
        Issue.issue_id.like(f'{prefix}-%')
    ).order_by(Issue.id.desc()).first()

    if latest:
        try:
            num = int(latest.issue_id.split('-')[1]) + 1
        except (IndexError, ValueError):
            num = 1001
    else:
        num = 1001

    return f'{prefix}-{num}'


def generate_consultation_id():
    """Generate a unique consultation ID. Format: CON-XXXX."""
    from app.models.consultation import Consultation
    latest = Consultation.query.order_by(Consultation.id.desc()).first()
    if latest:
        try:
            num = int(latest.consultation_id.split('-')[1]) + 1
        except (IndexError, ValueError):
            num = 1001
    else:
        num = 1001
    return f'CON-{num}'


def allowed_file(filename):
    """Check if a file extension is allowed."""
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', set())
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed


def save_upload(file, subfolder='issues'):
    """
    Save an uploaded file securely.
    Returns (filename, file_path) or (None, None) on failure.
    """
    if not file or not file.filename:
        return None, None

    if not allowed_file(file.filename):
        return None, None

    # Create unique filename
    ext = file.filename.rsplit('.', 1)[1].lower()
    unique_name = f'{uuid.uuid4().hex}.{ext}'
    safe_name = secure_filename(unique_name)

    upload_dir = os.path.join(
        current_app.config['UPLOAD_FOLDER'], subfolder
    )
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, safe_name)
    file.save(file_path)

    # Return the relative path for storage
    relative_path = f'uploads/{subfolder}/{safe_name}'
    return safe_name, relative_path


def format_datetime(dt, fmt='%d %b %Y, %I:%M %p'):
    """Format a datetime for display."""
    if dt is None:
        return ''
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime(fmt)


def format_date(dt, fmt='%d %b %Y'):
    """Format a date for display."""
    if dt is None:
        return ''
    return dt.strftime(fmt)


def time_ago(dt):
    """Return a human-readable time-ago string."""
    if dt is None:
        return ''
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    diff = now - dt
    seconds = diff.total_seconds()

    if seconds < 60:
        return 'Just now'
    elif seconds < 3600:
        mins = int(seconds / 60)
        return f'{mins} min ago'
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f'{hours} hr ago'
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f'{days} day{"s" if days > 1 else ""} ago'
    else:
        return format_date(dt)


def get_status_class(status):
    """Return a CSS class for issue status."""
    status_classes = {
        'Submitted': 'status-submitted',
        'Under Review': 'status-review',
        'Assigned': 'status-assigned',
        'In Progress': 'status-progress',
        'Waiting for Information': 'status-waiting',
        'Resolved': 'status-resolved',
        'Closed': 'status-closed',
    }
    return status_classes.get(status, 'status-default')


def get_priority_class(priority):
    """Return a CSS class for issue priority."""
    priority_classes = {
        'Low': 'priority-low',
        'Medium': 'priority-medium',
        'High': 'priority-high',
        'Critical': 'priority-critical',
    }
    return priority_classes.get(priority, 'priority-medium')
