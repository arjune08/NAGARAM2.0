"""
NAGARAM — Configuration
Flask configuration classes for development, testing, and production.
"""
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


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
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(BASE_DIR, "nagaram_dev.db")}'
    )


class ProductionConfig(Config):
    """Production configuration.

    Set DATABASE_URL to a persistent PostgreSQL database (for example Supabase).
    The /tmp fallback only keeps the Vercel function bootable when no database
    variable has been configured; Vercel /tmp storage is not persistent.
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
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
