"""
NAGARAM — NGO Routes
NGO dashboard, community issues, and coordination.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.issue import Issue, IssueComment, IssueUpdate
from app.models.notification import Notification
from app.forms.issue import CommentForm, IssueUpdateForm
from app.forms.expert import NGOUpdateForm
from app.services.issue_service import update_issue_status, get_issue_stats
from app.services.notification_service import get_user_notifications
from app.utils.decorators import role_required
from app.utils.helpers import get_status_class, get_priority_class, time_ago

ngo_bp = Blueprint('ngo', __name__)


@ngo_bp.before_request
@login_required
def before_request():
    pass


@ngo_bp.route('/dashboard')
@role_required('ngo')
def dashboard():
    stats = get_issue_stats(issue_type='civic')
    assigned = Issue.query.filter_by(
        assigned_to_id=current_user.id
    ).filter(Issue.status.notin_(['Resolved', 'Closed'])).all()

    community_issues = Issue.query.filter_by(
        issue_type='civic'
    ).filter(Issue.status.in_(['Submitted', 'Under Review'])).order_by(
        Issue.created_at.desc()
    ).limit(10).all()

    notifications = get_user_notifications(current_user.id, limit=5)

    return render_template('ngo/dashboard.html',
                           stats=stats, assigned=assigned,
                           community_issues=community_issues,
                           notifications=notifications,
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@ngo_bp.route('/community-issues')
@role_required('ngo')
def community_issues():
    status = request.args.get('status', '')
    query = Issue.query.filter_by(issue_type='civic')
    if status:
        query = query.filter_by(status=status)

    page = request.args.get('page', 1, type=int)
    issues = query.order_by(Issue.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('ngo/community_issues.html',
                           issues=issues,
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@ngo_bp.route('/assigned-issues')
@role_required('ngo')
def assigned_issues():
    query = Issue.query.filter_by(assigned_to_id=current_user.id)
    page = request.args.get('page', 1, type=int)
    issues = query.order_by(Issue.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('ngo/assigned_issues.html',
                           issues=issues,
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@ngo_bp.route('/issue/<int:issue_id>', methods=['GET', 'POST'])
@role_required('ngo')
def issue_detail(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    update_form = NGOUpdateForm()
    comment_form = CommentForm()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'volunteer':
            issue.assigned_to_id = current_user.id
            issue.status = 'Assigned'
            update = IssueUpdate(
                issue_id=issue.id, user_id=current_user.id,
                new_status='Assigned',
                message=f'NGO {current_user.full_name} volunteered to assist.',
                update_type='assignment',
            )
            db.session.add(update)
            notif = Notification(
                user_id=issue.reporter_id,
                title=f'Issue {issue.issue_id} Assigned',
                message=f'An NGO has volunteered to work on your issue.',
                notification_type='assignment',
                link=f'/citizen/issue/{issue.id}',
            )
            db.session.add(notif)
            db.session.commit()
            flash('You have volunteered to assist with this issue.', 'success')

        elif action == 'update' and update_form.validate():
            update_issue_status(
                issue, update_form.status.data, current_user,
                message=update_form.message.data,
            )
            flash('Update posted.', 'success')

        elif action == 'comment' and comment_form.validate():
            comment = IssueComment(
                issue_id=issue.id, user_id=current_user.id,
                content=comment_form.content.data,
            )
            db.session.add(comment)
            db.session.commit()
            flash('Comment added.', 'success')

        return redirect(url_for('ngo.issue_detail', issue_id=issue.id))

    updates = issue.updates.order_by(None).order_by(db.text('created_at ASC')).all()
    comments = issue.comments.all()
    images = issue.images.all()

    return render_template('ngo/issue_detail.html',
                           issue=issue, updates=updates, comments=comments,
                           images=images, update_form=update_form,
                           comment_form=comment_form,
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@ngo_bp.route('/completed')
@role_required('ngo')
def completed():
    issues = Issue.query.filter_by(
        assigned_to_id=current_user.id
    ).filter(Issue.status.in_(['Resolved', 'Closed'])).order_by(
        Issue.resolved_at.desc()
    ).all()
    return render_template('ngo/completed.html',
                           issues=issues,
                           get_status_class=get_status_class,
                           time_ago=time_ago)


@ngo_bp.route('/profile')
@role_required('ngo')
def profile():
    ngo_profile = current_user.ngo_profile
    assigned_count = Issue.query.filter_by(assigned_to_id=current_user.id).count()
    resolved_count = Issue.query.filter_by(
        assigned_to_id=current_user.id
    ).filter(Issue.status.in_(['Resolved', 'Closed'])).count()
    return render_template('ngo/profile.html',
                           ngo_profile=ngo_profile,
                           assigned_count=assigned_count,
                           resolved_count=resolved_count)
