"""
NAGARAM — Volunteer Routes
Volunteer dashboard, tasks, and contributions.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.issue import Issue, IssueComment, IssueUpdate
from app.models.notification import Notification
from app.forms.issue import CommentForm
from app.services.issue_service import update_issue_status
from app.services.notification_service import get_user_notifications
from app.utils.decorators import role_required
from app.utils.helpers import get_status_class, get_priority_class, time_ago

volunteer_bp = Blueprint('volunteer', __name__)


@volunteer_bp.before_request
@login_required
def before_request():
    pass


@volunteer_bp.route('/dashboard')
@role_required('volunteer')
def dashboard():
    my_tasks = Issue.query.filter_by(
        assigned_to_id=current_user.id
    ).filter(Issue.status.notin_(['Resolved', 'Closed'])).all()

    nearby = Issue.query.filter_by(
        issue_type='civic'
    ).filter(Issue.status.in_(['Submitted', 'Under Review', 'Assigned'])).order_by(
        Issue.created_at.desc()
    ).limit(10).all()

    completed_count = Issue.query.filter_by(
        assigned_to_id=current_user.id
    ).filter(Issue.status.in_(['Resolved', 'Closed'])).count()

    notifications = get_user_notifications(current_user.id, limit=5)

    return render_template('volunteer/dashboard.html',
                           my_tasks=my_tasks, nearby=nearby,
                           completed_count=completed_count,
                           notifications=notifications,
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@volunteer_bp.route('/nearby-issues')
@role_required('volunteer')
def nearby_issues():
    query = Issue.query.filter_by(issue_type='civic').filter(
        Issue.status.in_(['Submitted', 'Under Review', 'Assigned'])
    )
    page = request.args.get('page', 1, type=int)
    issues = query.order_by(Issue.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('volunteer/nearby_issues.html',
                           issues=issues,
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@volunteer_bp.route('/my-tasks')
@role_required('volunteer')
def my_tasks():
    tasks = Issue.query.filter_by(
        assigned_to_id=current_user.id
    ).filter(Issue.status.notin_(['Resolved', 'Closed'])).order_by(
        Issue.created_at.desc()
    ).all()
    return render_template('volunteer/my_tasks.html',
                           tasks=tasks,
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@volunteer_bp.route('/issue/<int:issue_id>', methods=['GET', 'POST'])
@role_required('volunteer')
def issue_detail(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    comment_form = CommentForm()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'volunteer':
            issue.assigned_to_id = current_user.id
            if issue.status in ('Submitted', 'Under Review'):
                issue.status = 'In Progress'
            update = IssueUpdate(
                issue_id=issue.id, user_id=current_user.id,
                new_status='In Progress',
                message=f'Volunteer {current_user.full_name} is working on this issue.',
                update_type='assignment',
            )
            db.session.add(update)
            db.session.commit()
            flash('You are now assigned to this issue.', 'success')

        elif action == 'complete':
            update_issue_status(issue, 'Resolved', current_user,
                                message='Volunteer has completed work on this issue.')
            flash('Issue marked as resolved.', 'success')

        elif action == 'comment' and comment_form.validate():
            comment = IssueComment(
                issue_id=issue.id, user_id=current_user.id,
                content=comment_form.content.data,
            )
            db.session.add(comment)
            db.session.commit()
            flash('Comment added.', 'success')

        return redirect(url_for('volunteer.issue_detail', issue_id=issue.id))

    updates = issue.updates.order_by(None).order_by(db.text('created_at ASC')).all()
    comments = issue.comments.all()

    return render_template('volunteer/issue_detail.html',
                           issue=issue, updates=updates, comments=comments,
                           comment_form=comment_form,
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@volunteer_bp.route('/contributions')
@role_required('volunteer')
def contributions():
    completed = Issue.query.filter_by(
        assigned_to_id=current_user.id
    ).filter(Issue.status.in_(['Resolved', 'Closed'])).order_by(
        Issue.resolved_at.desc()
    ).all()
    return render_template('volunteer/contributions.html',
                           contributions=completed,
                           get_status_class=get_status_class,
                           time_ago=time_ago)


@volunteer_bp.route('/profile')
@role_required('volunteer')
def profile():
    vol_profile = current_user.volunteer_profile
    task_count = Issue.query.filter_by(assigned_to_id=current_user.id).count()
    completed_count = Issue.query.filter_by(
        assigned_to_id=current_user.id
    ).filter(Issue.status.in_(['Resolved', 'Closed'])).count()
    return render_template('volunteer/profile.html',
                           volunteer_profile=vol_profile,
                           task_count=task_count,
                           completed_count=completed_count)
