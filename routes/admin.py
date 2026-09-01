"""
NAGARAM — Admin Routes
Admin dashboard, user management, issue management, analytics.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.user import User, Role
from app.models.issue import Issue, IssueCategory
from app.models.notification import Notification
from app.forms.issue import IssueUpdateForm, IssueAssignForm
from app.services.issue_service import update_issue_status, assign_issue, get_issue_stats
from app.utils.decorators import role_required, admin_required
from app.utils.helpers import get_status_class, get_priority_class, time_ago

admin_bp = Blueprint('admin', __name__)


@admin_bp.before_request
@login_required
def before_request():
    pass


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    civic_stats = get_issue_stats(issue_type='civic')
    agri_stats = get_issue_stats(issue_type='agricultural')
    total_stats = get_issue_stats()

    user_counts = {
        'total': User.query.count(),
        'citizens': User.query.join(Role).filter(Role.name == 'citizen').count(),
        'farmers': User.query.join(Role).filter(Role.name == 'farmer').count(),
        'experts': User.query.join(Role).filter(Role.name == 'expert').count(),
        'ngos': User.query.join(Role).filter(Role.name == 'ngo').count(),
        'volunteers': User.query.join(Role).filter(Role.name == 'volunteer').count(),
    }

    recent_issues = Issue.query.order_by(Issue.created_at.desc()).limit(10).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                           civic_stats=civic_stats,
                           agri_stats=agri_stats,
                           total_stats=total_stats,
                           user_counts=user_counts,
                           recent_issues=recent_issues,
                           recent_users=recent_users,
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@admin_bp.route('/users')
@admin_required
def users():
    role_filter = request.args.get('role', '')
    search = request.args.get('search', '')
    query = User.query.join(Role)

    if role_filter:
        query = query.filter(Role.name == role_filter)
    if search:
        s = f'%{search}%'
        query = query.filter(
            (User.full_name.ilike(s)) | (User.email.ilike(s)) | (User.username.ilike(s))
        )

    page = request.args.get('page', 1, type=int)
    users_list = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    roles = Role.query.all()

    return render_template('admin/users.html',
                           users=users_list, roles=roles,
                           role_filter=role_filter, search=search,
                           time_ago=time_ago)


@admin_bp.route('/users/<int:user_id>/toggle-active', methods=['POST'])
@admin_required
def toggle_user_active(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Cannot deactivate your own account.', 'error')
    else:
        user.is_active = not user.is_active
        db.session.commit()
        status = 'activated' if user.is_active else 'deactivated'
        flash(f'User {user.username} {status}.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/civic-issues')
@admin_required
def civic_issues():
    status = request.args.get('status', '')
    priority = request.args.get('priority', '')
    search = request.args.get('search', '')
    query = Issue.query.filter_by(issue_type='civic')

    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if search:
        s = f'%{search}%'
        query = query.filter(
            (Issue.title.ilike(s)) | (Issue.issue_id.ilike(s))
        )

    page = request.args.get('page', 1, type=int)
    issues = query.order_by(Issue.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    # Get NGOs and volunteers for assignment
    ngos = User.query.join(Role).filter(Role.name == 'ngo').all()
    volunteers = User.query.join(Role).filter(Role.name == 'volunteer').all()

    return render_template('admin/issues.html',
                           issues=issues, issue_type='civic',
                           title='Civic Issues',
                           ngos=ngos, volunteers=volunteers,
                           status=status, priority=priority, search=search,
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@admin_bp.route('/agricultural-issues')
@admin_required
def agricultural_issues():
    status = request.args.get('status', '')
    priority = request.args.get('priority', '')
    search = request.args.get('search', '')
    query = Issue.query.filter_by(issue_type='agricultural')

    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if search:
        s = f'%{search}%'
        query = query.filter(
            (Issue.title.ilike(s)) | (Issue.issue_id.ilike(s))
        )

    page = request.args.get('page', 1, type=int)
    issues = query.order_by(Issue.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    experts = User.query.join(Role).filter(Role.name == 'expert').all()

    return render_template('admin/issues.html',
                           issues=issues, issue_type='agricultural',
                           title='Agricultural Issues',
                           experts=experts,
                           status=status, priority=priority, search=search,
                           get_status_class=get_status_class,
                           get_priority_class=get_priority_class,
                           time_ago=time_ago)


@admin_bp.route('/issue/<int:issue_id>/assign', methods=['POST'])
@admin_required
def assign_issue_route(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    assigned_to_id = request.form.get('assigned_to_id', type=int)
    notes = request.form.get('notes', '')

    if not assigned_to_id:
        flash('Please select a user to assign.', 'error')
    else:
        assignee = User.query.get(assigned_to_id)
        role_type = assignee.role_name if assignee else ''
        assign_issue(issue, assigned_to_id, current_user, role_type, notes)
        flash(f'Issue {issue.issue_id} assigned to {assignee.full_name}.', 'success')

    if issue.issue_type == 'civic':
        return redirect(url_for('admin.civic_issues'))
    return redirect(url_for('admin.agricultural_issues'))


@admin_bp.route('/issue/<int:issue_id>/update-status', methods=['POST'])
@admin_required
def update_status(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    new_status = request.form.get('status')
    message = request.form.get('message', '')

    if new_status and new_status in Issue.STATUSES:
        update_issue_status(issue, new_status, current_user, message)
        flash(f'Issue {issue.issue_id} status updated to {new_status}.', 'success')

    if issue.issue_type == 'civic':
        return redirect(url_for('admin.civic_issues'))
    return redirect(url_for('admin.agricultural_issues'))


@admin_bp.route('/issue/<int:issue_id>/update-priority', methods=['POST'])
@admin_required
def update_priority(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    new_priority = request.form.get('priority')

    if new_priority and new_priority in Issue.PRIORITIES:
        issue.priority = new_priority
        db.session.commit()
        flash(f'Issue {issue.issue_id} priority updated to {new_priority}.', 'success')

    if issue.issue_type == 'civic':
        return redirect(url_for('admin.civic_issues'))
    return redirect(url_for('admin.agricultural_issues'))


@admin_bp.route('/categories', methods=['GET', 'POST'])
@admin_required
def categories():
    if request.method == 'POST':
        name = request.form.get('name')
        issue_type = request.form.get('issue_type')
        description = request.form.get('description', '')

        if name and issue_type:
            cat = IssueCategory(
                name=name, issue_type=issue_type, description=description
            )
            db.session.add(cat)
            db.session.commit()
            flash(f'Category "{name}" created.', 'success')

    civic_cats = IssueCategory.query.filter_by(issue_type='civic').all()
    agri_cats = IssueCategory.query.filter_by(issue_type='agricultural').all()

    return render_template('admin/categories.html',
                           civic_categories=civic_cats,
                           agri_categories=agri_cats)


@admin_bp.route('/analytics')
@admin_required
def analytics():
    civic_stats = get_issue_stats(issue_type='civic')
    agri_stats = get_issue_stats(issue_type='agricultural')
    total_stats = get_issue_stats()

    # Status distribution data for charts
    status_data = {}
    for status in Issue.STATUSES:
        status_data[status] = Issue.query.filter_by(status=status).count()

    # Category distribution
    categories = IssueCategory.query.all()
    cat_data = {}
    for cat in categories:
        count = Issue.query.filter_by(category_id=cat.id).count()
        if count > 0:
            cat_data[cat.name] = count

    return render_template('admin/analytics.html',
                           civic_stats=civic_stats,
                           agri_stats=agri_stats,
                           total_stats=total_stats,
                           status_data=status_data,
                           cat_data=cat_data)


@admin_bp.route('/settings')
@admin_required
def settings():
    return render_template('admin/settings.html')


# API endpoint for notification count
@admin_bp.route('/api/stats')
@admin_required
def api_stats():
    stats = get_issue_stats()
    return jsonify(stats)
