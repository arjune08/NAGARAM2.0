"""
NAGARAM — Main Routes
Landing page and public routes.
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def landing():
    """Landing page."""
    return render_template('main/landing.html')


@main_bp.route('/about')
def about():
    """About page."""
    return render_template('main/about.html')
