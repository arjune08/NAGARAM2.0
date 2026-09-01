"""
NAGARAM — Expert Routes
Expert dashboard, issue management, and consultation handling.
"""
from datetime import datetime, timezone
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.issue import Issue, IssueComment, IssueUpdate
from app.models.consultation import Consultation
from app.models.notification import Notification
from app.forms.issue import CommentForm, IssueUpdateForm
from app.forms.expert import DiagnosisForm, ExpertResponseForm
from app.services.issue_service import update_issue_status, get_issue_stats
from app.services.notification_service import get_user_notifications
from app.utils.decorators import role_required
from app.utils.helpers import get_status_class, get_priority_class, time_ago

expert_bp = Blueprint('expert', __name__)


@expert_bp.before_request
@login_required
def before_request():
    pass


@expert_bp.route('/dashboard')
@role_required('expert')
def dashboard():
    profile = current_user.expert_profile
    # Issues assigned to this expert
    assigned = Issue.query.filter_by(
        assigned_to_id=current_user.id, issue_type='agricultural'
    ).filter(Issue.status.notin_(['Resolved', 'Closed'])).all()

    # New unassigned agricultural issues
    new_issues = Issue.query.filter_by(
        issue_type='agricultural', status='Submitted'
    ).order_by(Issue.created_at.desc()).limit(10).all()

    # Pending consultations
    consultations = []
    if profile:
        consultations = Consultation.query.filter(
            (Consultation.expert_id == profile.id) |
            (Consultation.status == 'Pending')
        ).order_by(Consultation.created_at.desc()).limit(10).all()

    stats = get_issue_stats(issue_type='agricultural')
    notifications = get_user_notifications(current_user.id, limit=5)

    return render_template('expert/dashboard.html',
                           assigned=assigned, new_issues=new_issues,
                           consultations=consultations, stats=stats,
                           notifications=notifications,
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@expert_bp.route('/new-issues')
@role_required('expert')
def new_issues():
    category = request.args.get('category', '')
    query = Issue.query.filter_by(issue_type='agricultural')
    query = query.filter(Issue.status.in_(['Submitted', 'Under Review']))

    if category:
        query = query.filter(Issue.category.has(name=category))

    page = request.args.get('page', 1, type=int)
    issues = query.order_by(Issue.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('expert/issues.html',
                           issues=issues, title='New Issues',
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@expert_bp.route('/assigned-issues')
@role_required('expert')
def assigned_issues():
    query = Issue.query.filter_by(
        assigned_to_id=current_user.id, issue_type='agricultural'
    ).filter(Issue.status.notin_(['Resolved', 'Closed']))
    page = request.args.get('page', 1, type=int)
    issues = query.order_by(Issue.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('expert/issues.html',
                           issues=issues, title='Assigned Issues',
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@expert_bp.route('/resolved-issues')
@role_required('expert')
def resolved_issues():
    query = Issue.query.filter_by(
        resolved_by_id=current_user.id
    )
    page = request.args.get('page', 1, type=int)
    issues = query.order_by(Issue.resolved_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('expert/issues.html',
                           issues=issues, title='Resolved Issues',
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@expert_bp.route('/issue/<int:issue_id>', methods=['GET', 'POST'])
@role_required('expert')
def issue_detail(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    update_form = IssueUpdateForm()
    comment_form = CommentForm()
    diagnosis_form = DiagnosisForm()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'accept':
            issue.assigned_to_id = current_user.id
            issue.status = 'In Progress'
            update = IssueUpdate(
                issue_id=issue.id, user_id=current_user.id,
                old_status='Submitted', new_status='In Progress',
                message=f'Issue accepted by expert {current_user.full_name}.',
                update_type='assignment',
            )
            db.session.add(update)
            # Notify farmer
            notif = Notification(
                user_id=issue.reporter_id,
                title=f'Expert Assigned to {issue.issue_id}',
                message=f'Expert {current_user.full_name} is now working on your issue.',
                notification_type='assignment',
                link=f'/farmer/crop-health',
            )
            db.session.add(notif)
            db.session.commit()
            flash('Issue accepted.', 'success')

        elif action == 'update_status' and update_form.validate():
            update_issue_status(
                issue, update_form.status.data, current_user,
                message=update_form.message.data,
                resolution=update_form.resolution.data,
            )
            flash('Issue updated.', 'success')

        elif action == 'diagnose' and diagnosis_form.validate():
            issue.resolution = (
                f'**Diagnosis:** {diagnosis_form.diagnosis.data}\n\n'
                f'**Recommendation:** {diagnosis_form.recommendation.data}'
            )
            issue.status = 'Resolved'
            issue.resolved_at = datetime.now(timezone.utc)
            issue.resolved_by_id = current_user.id

            update = IssueUpdate(
                issue_id=issue.id, user_id=current_user.id,
                old_status=issue.status, new_status='Resolved',
                message=f'Expert diagnosis and recommendation provided.',
                update_type='resolution',
            )
            db.session.add(update)
            notif = Notification(
                user_id=issue.reporter_id,
                title=f'Issue {issue.issue_id} Resolved',
                message=f'Expert has provided diagnosis and recommendation for your issue.',
                notification_type='resolution',
                link=f'/farmer/crop-health',
            )
            db.session.add(notif)
            db.session.commit()
            flash('Diagnosis submitted and issue resolved.', 'success')

        elif action == 'comment' and comment_form.validate():
            comment = IssueComment(
                issue_id=issue.id, user_id=current_user.id,
                content=comment_form.content.data,
            )
            db.session.add(comment)
            db.session.commit()
            flash('Comment added.', 'success')

        return redirect(url_for('expert.issue_detail', issue_id=issue.id))

    updates = issue.updates.order_by(None).order_by(db.text('created_at ASC')).all()
    comments = issue.comments.all()
    images = issue.images.all()

    return render_template('expert/issue_detail.html',
                           issue=issue, updates=updates, comments=comments,
                           images=images, update_form=update_form,
                           comment_form=comment_form,
                           diagnosis_form=diagnosis_form,
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@expert_bp.route('/consultations')
@role_required('expert')
def consultations():
    profile = current_user.expert_profile
    query = Consultation.query
    if profile:
        query = query.filter(
            (Consultation.expert_id == profile.id) |
            (Consultation.status == 'Pending')
        )
    consults = query.order_by(Consultation.created_at.desc()).all()
    return render_template('expert/consultations.html',
                           consultations=consults, time_ago=time_ago)


@expert_bp.route('/consultation/<int:consult_id>', methods=['GET', 'POST'])
@role_required('expert')
def consultation_detail(consult_id):
    consultation = Consultation.query.get_or_404(consult_id)
    form = ExpertResponseForm()

    if form.validate_on_submit():
        profile = current_user.expert_profile
        consultation.expert_id = profile.id if profile else None
        consultation.diagnosis = form.diagnosis.data
        consultation.recommendation = form.recommendation.data
        consultation.status = form.status.data
        consultation.answered_at = datetime.now(timezone.utc)
        db.session.commit()

        # Notify farmer
        notif = Notification(
            user_id=consultation.farmer.user_id,
            title=f'Consultation {consultation.consultation_id} Answered',
            message=f'An expert has responded to your query: "{consultation.subject}".',
            notification_type='resolution',
            link='/farmer/advisor',
        )
        db.session.add(notif)
        db.session.commit()
        flash('Response submitted.', 'success')
        return redirect(url_for('expert.consultations'))

    return render_template('expert/consultation_detail.html',
                           consultation=consultation, form=form,
                           time_ago=time_ago)


@expert_bp.route('/profile')
@role_required('expert')
def profile():
    ep = current_user.expert_profile
    resolved_count = Issue.query.filter_by(resolved_by_id=current_user.id).count()
    return render_template('expert/profile.html',
                           expert_profile=ep, resolved_count=resolved_count)
