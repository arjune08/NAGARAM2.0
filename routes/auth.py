"""
NAGARAM — Authentication Routes
Login, registration, and logout.
"""
from datetime import datetime, timezone
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User, Role
from app.models.profile import (
    CitizenProfile, FarmerProfile, ExpertProfile,
    NGOProfile, VolunteerProfile
)
from app.forms.auth import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if current_user.is_authenticated:
        return redirect(current_user.get_dashboard_url())

    form = LoginForm()
    if form.validate_on_submit():
        # Try email or username
        user = User.query.filter(
            (User.email == form.login.data) | (User.username == form.login.data)
        ).first()

        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Your account has been deactivated. Contact admin.', 'error')
                return render_template('auth/login.html', form=form)

            login_user(user, remember=form.remember_me.data)
            user.last_login = datetime.now(timezone.utc)
            db.session.commit()

            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(user.get_dashboard_url())
        else:
            flash('Invalid email/username or password.', 'error')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if current_user.is_authenticated:
        return redirect(current_user.get_dashboard_url())

    form = RegistrationForm()
    if form.validate_on_submit():
        # Get or create role
        role = Role.get_or_create(form.role.data)

        user = User(
            email=form.email.data,
            username=form.username.data,
            full_name=form.full_name.data,
            phone=form.phone.data,
            role_id=role.id,
            location=form.location.data,
            district=form.district.data,
            state=form.state.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()

        # Create role-specific profile
        _create_role_profile(user, form.role.data)

        db.session.commit()
        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.landing'))


def _create_role_profile(user, role_name):
    """Create the appropriate role-specific profile for a new user."""
    profiles = {
        'citizen': CitizenProfile(user_id=user.id),
        'farmer': FarmerProfile(user_id=user.id),
        'expert': ExpertProfile(user_id=user.id, expertise_area='general'),
        'ngo': NGOProfile(user_id=user.id, organization_name=user.full_name),
        'volunteer': VolunteerProfile(user_id=user.id),
    }
    profile = profiles.get(role_name)
    if profile:
        db.session.add(profile)
