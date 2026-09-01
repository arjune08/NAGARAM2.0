"""NAGARAM Flask application package.

The application factory lives here so Vercel can import ``app`` directly
without depending on the legacy root-level ``__init__.py`` module.
"""
import os
from flask import Flask, render_template
from config import config
from app.extensions import db, login_manager, csrf


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')


# Demo accounts are intentionally deterministic so a fresh deployment can be
# tested immediately.  They are only for the application's demo environment;
# real users should register their own accounts.
DEMO_USERS = [
    {
        'username': 'admin',
        'email': 'admin@nagaram.gov.in',
        'full_name': 'System Administrator',
        'role_name': 'admin',
        'phone': '9876543210',
        'location': 'New Delhi',
        'district': 'Central Delhi',
        'state': 'Delhi',
    },
    {
        'username': 'citizen1',
        'email': 'citizen@nagaram.gov.in',
        'full_name': 'Rajesh Kumar',
        'role_name': 'citizen',
        'phone': '9876543211',
        'location': 'Connaught Place',
        'district': 'Central Delhi',
        'state': 'Delhi',
    },
    {
        'username': 'farmer1',
        'email': 'farmer@nagaram.gov.in',
        'full_name': 'Ramesh Singh',
        'role_name': 'farmer',
        'phone': '9876543212',
        'location': 'Karnal',
        'district': 'Karnal',
        'state': 'Haryana',
    },
    {
        'username': 'expert1',
        'email': 'expert@nagaram.gov.in',
        'full_name': 'Dr. Anita Sharma',
        'role_name': 'expert',
        'phone': '9876543213',
        'location': 'Pusa',
        'district': 'New Delhi',
        'state': 'Delhi',
    },
    {
        'username': 'ngo1',
        'email': 'ngo@nagaram.gov.in',
        'full_name': 'Jan Seva Foundation',
        'role_name': 'ngo',
        'phone': '9876543214',
        'location': 'Jaipur',
        'district': 'Jaipur',
        'state': 'Rajasthan',
    },
    {
        'username': 'volunteer1',
        'email': 'volunteer@nagaram.gov.in',
        'full_name': 'Suresh Patel',
        'role_name': 'volunteer',
        'phone': '9876543215',
        'location': 'Ahmedabad',
        'district': 'Ahmedabad',
        'state': 'Gujarat',
    },
]


def _ensure_demo_users():
    """Create/reset the deterministic demo accounts idempotently.

    This runs after ``db.create_all()`` so a new production database and a
    temporary Vercel fallback database both have usable demo credentials.
    Existing demo accounts are reactivated and their demo password is kept in
    sync, while unrelated user accounts are left untouched.
    """
    from app.models.user import User, Role
    from app.models.profile import (
        CitizenProfile, FarmerProfile, ExpertProfile,
        NGOProfile, VolunteerProfile,
    )

    for data in DEMO_USERS:
        role = Role.query.filter_by(name=data['role_name']).first()
        if role is None:
            continue

        user = User.query.filter(
            (User.email == data['email']) | (User.username == data['username'])
        ).first()

        if user is None:
            user = User(
                username=data['username'],
                email=data['email'],
                full_name=data['full_name'],
                role_id=role.id,
                phone=data['phone'],
                location=data['location'],
                district=data['district'],
                state=data['state'],
                is_active=True,
                is_verified=True,
            )
            user.set_password('demo123')
            db.session.add(user)
            db.session.flush()
        else:
            # These are reserved demo identities, so make sure the documented
            # credentials continue to work after redeployments.
            changed = False
            if user.role_id != role.id:
                user.role_id = role.id
                changed = True
            if not user.is_active:
                user.is_active = True
                changed = True
            if not user.is_verified:
                user.is_verified = True
                changed = True
            if not user.check_password('demo123'):
                user.set_password('demo123')
                changed = True
            if changed:
                db.session.add(user)

        # Add the role-specific profile if a previous partial seed did not
        # create it.  This keeps demo dashboard pages from failing after login.
        profile_map = {
            'citizen': (CitizenProfile, {}),
            'farmer': (FarmerProfile, {
                'farming_type': 'Organic',
                'land_holding': 5.5,
                'primary_crop': 'Rice (Paddy)',
                'secondary_crops': 'Wheat, Sugarcane',
            }),
            'expert': (ExpertProfile, {
                'expertise_area': 'Crop Pathology',
                'specialization': 'Pest & Disease Management',
                'qualification': 'Ph.D in Agronomy',
                'experience_years': 12,
                'institution': 'Indian Agricultural Research Institute',
            }),
            'ngo': (NGOProfile, {
                'organization_name': 'Jan Seva Foundation',
                'registration_number': 'NGO-2020-8849',
                'focus_areas': 'Rural Infrastructure, Water Harvesting',
                'service_districts': 'Jaipur, Alwar, Dausa',
            }),
            'volunteer': (VolunteerProfile, {
                'skills': 'First Aid, Survey, Community Outreach',
                'availability': 'Weekends',
            }),
        }
        profile_spec = profile_map.get(data['role_name'])
        if profile_spec:
            profile_model, profile_values = profile_spec
            if not profile_model.query.filter_by(user_id=user.id).first():
                db.session.add(profile_model(user_id=user.id, **profile_values))

    db.session.commit()


def create_app(config_name=None):
    """Create and configure the Flask application.

    Templates and static assets live at the repository root, while this
    application factory lives under ``app/``. Flask otherwise searches under
    ``app/templates`` and ``app/static`` when initialized with ``Flask(__name__)``.
    Explicit paths keep local and Vercel deployments consistent.
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(
        __name__,
        template_folder=TEMPLATE_DIR,
        static_folder=STATIC_DIR,
        static_url_path='/static',
    )
    app.config.from_object(config.get(config_name, config['default']))

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    upload_dir = app.config.get('UPLOAD_FOLDER')
    if upload_dir:
        os.makedirs(upload_dir, exist_ok=True)

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    _register_blueprints(app)
    _register_error_handlers(app)

    from app.commands import seed_cli
    app.cli.add_command(seed_cli)

    with app.app_context():
        db.create_all()
        try:
            from app.models.user import Role
            from app.models.issue import IssueCategory
            from app.models.scheme import GovernmentScheme

            if Role.query.count() == 0:
                Role.seed_default_roles()
            if IssueCategory.query.count() == 0:
                IssueCategory.seed_default_categories()
            if GovernmentScheme.query.count() == 0:
                GovernmentScheme.seed_default_schemes()

            # Unlike the larger demo-data command, this lightweight seed is
            # safe to run on every application startup and guarantees that the
            # published demo credentials can actually authenticate.
            _ensure_demo_users()
        except Exception as e:
            # A database connectivity problem should not prevent the landing
            # page from booting. Real production persistence still requires a
            # valid DATABASE_URL.
            app.logger.warning(f"Auto-seeding skipped or failed: {e}")

    @app.context_processor
    def inject_globals():
        from flask_login import current_user
        unread = 0
        if current_user.is_authenticated:
            from app.models.notification import Notification
            unread = Notification.query.filter_by(
                user_id=current_user.id, is_read=False
            ).count()
        return dict(unread_notifications=unread)

    return app


def _register_blueprints(app):
    """Register all route blueprints."""
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.citizen import citizen_bp
    from app.routes.farmer import farmer_bp
    from app.routes.expert import expert_bp
    from app.routes.ngo import ngo_bp
    from app.routes.volunteer import volunteer_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(citizen_bp, url_prefix='/citizen')
    app.register_blueprint(farmer_bp, url_prefix='/farmer')
    app.register_blueprint(expert_bp, url_prefix='/expert')
    app.register_blueprint(ngo_bp, url_prefix='/ngo')
    app.register_blueprint(volunteer_bp, url_prefix='/volunteer')
    app.register_blueprint(admin_bp, url_prefix='/admin')


def _register_error_handlers(app):
    """Register custom error pages."""
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500


__all__ = ["create_app"]
