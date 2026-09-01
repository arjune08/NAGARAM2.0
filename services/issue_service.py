"""
NAGARAM — Issue Service
Business logic for issue management.
"""
from datetime import datetime, timezone
from app.extensions import db
from app.models.issue import Issue, IssueUpdate, IssueAssignment, IssueImage
from app.models.notification import Notification
from app.utils.helpers import generate_issue_id


def create_issue(form_data, reporter, issue_type='civic', images=None):
    """
    Create a new issue from form data.
    Returns the created Issue object.
    """
    issue = Issue(
        issue_id=generate_issue_id(issue_type),
        issue_type=issue_type,
        title=form_data.get('title'),
        description=form_data.get('description'),
        category_id=form_data.get('category_id'),
        reporter_id=reporter.id,
        reporter_type=reporter.role_name,
        location=form_data.get('location'),
        district=form_data.get('district'),
        state=form_data.get('state'),
        pincode=form_data.get('pincode'),
        latitude=form_data.get('latitude') or None,
        longitude=form_data.get('longitude') or None,
        priority=form_data.get('priority', 'Medium'),
        crop_name=form_data.get('crop_name'),
        affected_area=form_data.get('affected_area'),
        farm_id=form_data.get('farm_id') or None,
        status='Submitted',
    )
    db.session.add(issue)
    db.session.flush()  # Get the ID before committing

    # Save images
    if images:
        from app.utils.helpers import save_upload
        for img_file in images:
            if img_file and img_file.filename:
                filename, file_path = save_upload(img_file, 'issues')
                if filename:
                    img = IssueImage(
                        issue_id=issue.id,
                        filename=filename,
                        original_filename=img_file.filename,
                        file_path=file_path,
                        uploaded_by_id=reporter.id,
                    )
                    db.session.add(img)

    # Create initial update
    update = IssueUpdate(
        issue_id=issue.id,
        user_id=reporter.id,
        new_status='Submitted',
        message=f'Issue {issue.issue_id} submitted.',
        update_type='status_change',
    )
    db.session.add(update)
    db.session.commit()

    return issue


def update_issue_status(issue, new_status, user, message='', resolution=''):
    """Update an issue's status and create an update record."""
    old_status = issue.status
    issue.status = new_status
    issue.updated_at = datetime.now(timezone.utc)

    if new_status == 'Resolved':
        issue.resolved_at = datetime.now(timezone.utc)
        issue.resolved_by_id = user.id
        if resolution:
            issue.resolution = resolution

    update = IssueUpdate(
        issue_id=issue.id,
        user_id=user.id,
        old_status=old_status,
        new_status=new_status,
        message=message or f'Status changed from {old_status} to {new_status}.',
        update_type='status_change',
    )
    db.session.add(update)

    # Notify the reporter
    _notify_status_change(issue, old_status, new_status)

    db.session.commit()
    return update


def assign_issue(issue, assigned_to_id, assigned_by, role_type='', notes=''):
    """Assign an issue to a user/organization."""
    assignment = IssueAssignment(
        issue_id=issue.id,
        assigned_to_id=assigned_to_id,
        assigned_by_id=assigned_by.id,
        role_type=role_type,
        notes=notes,
    )
    db.session.add(assignment)

    issue.assigned_to_id = assigned_to_id
    if issue.status == 'Submitted' or issue.status == 'Under Review':
        issue.status = 'Assigned'
    issue.updated_at = datetime.now(timezone.utc)

    # Create update
    from app.models.user import User
    assignee = db.session.get(User, assigned_to_id)
    assignee_name = assignee.full_name if assignee else 'Unknown'

    update = IssueUpdate(
        issue_id=issue.id,
        user_id=assigned_by.id,
        old_status=issue.status,
        new_status='Assigned',
        message=f'Issue assigned to {assignee_name}.',
        update_type='assignment',
    )
    db.session.add(update)

    # Notify assignee
    notif = Notification(
        user_id=assigned_to_id,
        title='New Issue Assigned',
        message=f'Issue {issue.issue_id}: "{issue.title}" has been assigned to you.',
        notification_type='assignment',
        link=f'/{"expert" if role_type == "expert" else "ngo"}/issue/{issue.id}',
    )
    db.session.add(notif)

    # Notify reporter
    notif2 = Notification(
        user_id=issue.reporter_id,
        title='Issue Assigned',
        message=f'Your issue {issue.issue_id} has been assigned to {assignee_name}.',
        notification_type='status_change',
        link=f'/citizen/issue/{issue.id}',
    )
    db.session.add(notif2)

    db.session.commit()
    return assignment


def get_issue_stats(issue_type=None, user_id=None):
    """Get issue statistics for dashboards."""
    query = Issue.query
    if issue_type:
        query = query.filter_by(issue_type=issue_type)
    if user_id:
        query = query.filter_by(reporter_id=user_id)

    total = query.count()
    submitted = query.filter_by(status='Submitted').count()
    under_review = query.filter_by(status='Under Review').count()
    assigned = query.filter_by(status='Assigned').count()
    in_progress = query.filter_by(status='In Progress').count()
    resolved = query.filter_by(status='Resolved').count()
    closed = query.filter_by(status='Closed').count()

    return {
        'total': total,
        'submitted': submitted,
        'under_review': under_review,
        'assigned': assigned,
        'in_progress': in_progress,
        'open': submitted + under_review + assigned + in_progress,
        'resolved': resolved,
        'closed': closed,
    }


def _notify_status_change(issue, old_status, new_status):
    """Create notification for issue status change."""
    notif = Notification(
        user_id=issue.reporter_id,
        title=f'Issue {issue.issue_id} Updated',
        message=f'Your issue "{issue.title}" status changed from {old_status} to {new_status}.',
        notification_type='status_change',
        link=f'/citizen/issue/{issue.id}',
    )
    db.session.add(notif)
