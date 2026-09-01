"""
NAGARAM — User & Role Models
Core authentication models with role-based access control.
"""
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db


class Role(db.Model):
    """User roles: citizen, farmer, expert, ngo, volunteer, admin."""
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False, index=True)
    description = db.Column(db.String(200))

    users = db.relationship('User', backref='role', lazy='dynamic')

    CITIZEN = 'citizen'
    FARMER = 'farmer'
    EXPERT = 'expert'
    NGO = 'ngo'
    VOLUNTEER = 'volunteer'
    ADMIN = 'admin'

    @classmethod
    def seed_default_roles(cls):
        """Seed all 6 default roles."""
        default_roles = [
            (cls.CITIZEN, 'General citizen reporting civic issues'),
            (cls.FARMER, 'Agricultural producer'),
            (cls.EXPERT, 'Agricultural expert or extension worker'),
            (cls.NGO, 'Non-governmental organization'),
            (cls.VOLUNTEER, 'Community volunteer'),
            (cls.ADMIN, 'System administrator'),
        ]
        created = []
        for name, desc in default_roles:
            role = cls.get_or_create(name, desc)
            created.append(role)
        return created

    @staticmethod
    def get_or_create(name, description=''):
        """Get existing role or create a new one."""
        role = Role.query.filter_by(name=name).first()
        if role is None:
            role = Role(name=name, description=description)
            db.session.add(role)
            db.session.commit()
        return role

    def __repr__(self):
        return f'<Role {self.name}>'


class User(UserMixin, db.Model):
    """Platform user with role-based authentication."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    avatar_url = db.Column(db.String(500))
    location = db.Column(db.String(200))
    district = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(10))
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    last_login = db.Column(db.DateTime)

    # Relationships
    issues = db.relationship('Issue', backref='reporter', lazy='dynamic',
                             foreign_keys='Issue.reporter_id')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the user's password."""
        return check_password_hash(self.password_hash, password)

    @property
    def role_name(self):
        """Get the user's role name."""
        return self.role.name if self.role else None

    def has_role(self, role_name):
        """Check if user has a specific role."""
        return self.role_name == role_name

    def is_admin(self):
        """Check if user is an admin."""
        return self.has_role(Role.ADMIN)

    def get_dashboard_url(self):
        """Return the appropriate dashboard URL for this user's role."""
        role_dashboards = {
            Role.CITIZEN: '/citizen/dashboard',
            Role.FARMER: '/farmer/dashboard',
            Role.EXPERT: '/expert/dashboard',
            Role.NGO: '/ngo/dashboard',
            Role.VOLUNTEER: '/volunteer/dashboard',
            Role.ADMIN: '/admin/dashboard',
        }
        return role_dashboards.get(self.role_name, '/')

    def __repr__(self):
        return f'<User {self.username} ({self.role_name})>'
