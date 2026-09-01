"""NAGARAM Flask application package.

The application factory lives here so Vercel can import ``app`` directly
without depending on the legacy root-level ``__init__.py`` module.
"""
import os
from flask import Flask, render_template
from config import config
from app.extensions import db, login_manager, csrf


def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__)
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
        except Exception as e:
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
