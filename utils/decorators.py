"""
NAGARAM — Route Decorators
Role-based access control decorators.
"""
from functools import wraps
from flask import abort
from flask_login import current_user


def role_required(*roles):
    """
    Decorator to restrict route access to specific roles.
    Usage: @role_required('admin', 'expert')
    Returns 403 if user lacks the required role.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role_name not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Shortcut decorator for admin-only routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
