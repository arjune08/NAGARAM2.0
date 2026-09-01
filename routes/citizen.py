"""
NAGARAM — Citizen Routes
Citizen dashboard, issue reporting, tracking, and profile.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.issue import Issue, IssueCategory, IssueComment
from app.models.notification import Notification
from app.forms.issue import CivicIssueForm, CommentForm, IssueFilterForm
from app.services.issue_service import create_issue, get_issue_stats
from app.services.notification_service import get_user_notifications, mark_as_read, mark_all_as_read
from app.utils.decorators import role_required
from app.utils.helpers import get_status_class, get_priority_class, time_ago

citizen_bp = Blueprint('citizen', __name__)


@citizen_bp.before_request
@login_required
def before_request():
    """Ensure user is authenticated."""
    pass


@citizen_bp.route('/dashboard')
@role_required('citizen')
def dashboard():
    """Citizen dashboard."""
    stats = get_issue_stats(issue_type='civic', user_id=current_user.id)
    recent_issues = Issue.query.filter_by(
        reporter_id=current_user.id, issue_type='civic'
    ).order_by(Issue.created_at.desc()).limit(5).all()
    notifications = get_user_notifications(current_user.id, limit=5)

    return render_template('citizen/dashboard.html',
                           stats=stats,
                           recent_issues=recent_issues,
                           notifications=notifications,
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@citizen_bp.route('/report-issue', methods=['GET', 'POST'])
@role_required('citizen')
def report_issue():
    """Report a new civic issue."""
    form = CivicIssueForm()
    categories = IssueCategory.query.filter_by(
        issue_type='civic', is_active=True
    ).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        form_data = {
            'title': form.title.data,
            'description': form.description.data,
            'category_id': form.category_id.data,
            'location': form.location.data,
            'district': form.district.data,
            'state': form.state.data,
            'pincode': form.pincode.data,
            'latitude': form.latitude.data,
            'longitude': form.longitude.data,
            'priority': form.priority.data,
        }
        images = request.files.getlist('images')
        issue = create_issue(form_data, current_user, 'civic', images)
        flash(f'Issue {issue.issue_id} submitted successfully.', 'success')
        return redirect(url_for('citizen.issue_detail', issue_id=issue.id))

    return render_template('citizen/report_issue.html', form=form)


@citizen_bp.route('/my-issues')
@role_required('citizen')
def my_issues():
    """List of citizen's reported issues."""
    filter_form = IssueFilterForm(request.args)
    query = Issue.query.filter_by(
        reporter_id=current_user.id, issue_type='civic'
    )

    # Apply filters
    if filter_form.status.data:
        query = query.filter_by(status=filter_form.status.data)
    if filter_form.priority.data:
        query = query.filter_by(priority=filter_form.priority.data)
    if filter_form.search.data:
        search = f'%{filter_form.search.data}%'
        query = query.filter(
            (Issue.title.ilike(search)) | (Issue.description.ilike(search))
        )

    # Sort
    sort = filter_form.sort.data or 'newest'
    if sort == 'oldest':
        query = query.order_by(Issue.created_at.asc())
    elif sort == 'priority':
        query = query.order_by(Issue.priority.desc())
    else:
        query = query.order_by(Issue.created_at.desc())

    page = request.args.get('page', 1, type=int)
    issues = query.paginate(page=page, per_page=10, error_out=False)

    return render_template('citizen/my_issues.html',
                           issues=issues, filter_form=filter_form,
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@citizen_bp.route('/issue/<int:issue_id>', methods=['GET', 'POST'])
@role_required('citizen')
def issue_detail(issue_id):
    """View issue details."""
    issue = Issue.query.get_or_404(issue_id)
    if issue.reporter_id != current_user.id:
        flash('You can only view your own issues.', 'error')
        return redirect(url_for('citizen.my_issues'))

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = IssueComment(
            issue_id=issue.id,
            user_id=current_user.id,
            content=comment_form.content.data,
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment added.', 'success')
        return redirect(url_for('citizen.issue_detail', issue_id=issue.id))

    updates = issue.updates.order_by(None).order_by(
        db.text('created_at ASC')
    ).all()
    comments = issue.comments.all()
    images = issue.images.all()

    return render_template('citizen/issue_detail.html',
                           issue=issue, updates=updates,
                           comments=comments, images=images,
                           comment_form=comment_form,
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@citizen_bp.route('/notifications')
@role_required('citizen')
def notifications():
    """View notifications."""
    notifs = get_user_notifications(current_user.id, limit=50)
    return render_template('citizen/notifications.html',
                           notifications=notifs, time_ago=time_ago)


@citizen_bp.route('/notifications/read/<int:notif_id>')
@role_required('citizen')
def read_notification(notif_id):
    """Mark notification as read and redirect."""
    notif = mark_as_read(notif_id, current_user.id)
    if notif and notif.link:
        return redirect(notif.link)
    return redirect(url_for('citizen.notifications'))


@citizen_bp.route('/notifications/read-all')
@role_required('citizen')
def read_all_notifications():
    """Mark all notifications as read."""
    mark_all_as_read(current_user.id)
    flash('All notifications marked as read.', 'success')
    return redirect(url_for('citizen.notifications'))


@citizen_bp.route('/profile')
@role_required('citizen')
def profile():
    """Citizen profile page."""
    stats = get_issue_stats(issue_type='civic', user_id=current_user.id)
    return render_template('citizen/profile.html', stats=stats)
