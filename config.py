"""
NAGARAM — Configuration
Flask configuration classes for development, testing, and production.
"""
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def _database_url_from_env(default=None):
    """Return a usable DATABASE_URL, ignoring common placeholder values.

    This prevents a copied Supabase example such as
    ``db.YOUR_PROJECT.supabase.co`` from crashing the Vercel function during
    application startup. A real production deployment should set DATABASE_URL
    to the connection string for the NAGARAM Supabase project.
    """
    value = (os.environ.get("DATABASE_URL") or "").strip()
    if not value:
        return default

    placeholder_markers = (
        "YOUR_PROJECT",
        "your-project",
        "PROJECT_REF",
        "YOUR_PASSWORD",
        "YOUR_DB_PASSWORD",
    )
    if any(marker in value for marker in placeholder_markers):
        return default

    return value


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'nagaram-dev-secret-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    # Vercel's deployed filesystem is read-only; /tmp is writable but ephemeral.
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/tmp/nagaram_uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf'}
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    ITEMS_PER_PAGE = 20


class DevelopmentConfig(Config):
    """Development configuration — uses SQLite by default."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = _database_url_from_env(
        f'sqlite:///{os.path.join(BASE_DIR, "nagaram_dev.db")}'
    )


class ProductionConfig(Config):
    """Production configuration.

    A valid DATABASE_URL should point to the persistent Supabase PostgreSQL
    database. If the environment still contains an example/placeholder URL,
    fall back to an ephemeral SQLite database so Vercel can boot instead of
    returning an import/startup 500. The SQLite fallback is deliberately only
    a resilience fallback; it is not a replacement for production storage.
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = _database_url_from_env(
        'sqlite:////tmp/nagaram_vercel.db'
    )
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_TIME_LIMIT = 3600

    @classmethod
    def init_app(cls, app):
        uri = app.config.get('SQLALCHEMY_DATABASE_URI', '') or ''
        if uri.startswith('postgres://'):
            app.config['SQLALCHEMY_DATABASE_URI'] = uri.replace(
                'postgres://', 'postgresql://', 1
            )


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
