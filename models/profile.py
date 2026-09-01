"""
NAGARAM — Role-Specific Profile Models
Extended profile information for each user role.
"""
from datetime import datetime, timezone
from app.extensions import db


class CitizenProfile(db.Model):
    """Extended profile for citizens."""
    __tablename__ = 'citizen_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    address = db.Column(db.Text)
    ward_number = db.Column(db.String(20))
    municipality = db.Column(db.String(100))
    issues_reported = db.Column(db.Integer, default=0)
    issues_resolved = db.Column(db.Integer, default=0)

    user = db.relationship('User', backref=db.backref('citizen_profile', uselist=False))

    def __repr__(self):
        return f'<CitizenProfile user_id={self.user_id}>'


class FarmerProfile(db.Model):
    """Extended profile for farmers."""
    __tablename__ = 'farmer_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    farmer_id = db.Column(db.String(50), unique=True)  # Government farmer ID
    land_holding = db.Column(db.Float)  # Acres
    land_type = db.Column(db.String(50))  # Irrigated, Rain-fed, Mixed
    primary_crop = db.Column(db.String(100))
    secondary_crops = db.Column(db.String(300))
    farming_type = db.Column(db.String(50))  # Organic, Conventional, Mixed
    experience_years = db.Column(db.Integer)
    bank_account = db.Column(db.String(20))
    aadhar_linked = db.Column(db.Boolean, default=False)
    preferred_language = db.Column(db.String(20), default='en')

    user = db.relationship('User', backref=db.backref('farmer_profile', uselist=False))
    farms = db.relationship('Farm', backref='farmer', lazy='dynamic')

    def __repr__(self):
        return f'<FarmerProfile user_id={self.user_id}>'


class ExpertProfile(db.Model):
    """Extended profile for agricultural/civic experts."""
    __tablename__ = 'expert_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    expertise_area = db.Column(db.String(100), nullable=False)
    # crop, soil, irrigation, pest_disease, advisory, market
    specialization = db.Column(db.String(200))
    qualification = db.Column(db.String(200))
    institution = db.Column(db.String(200))
    experience_years = db.Column(db.Integer)
    license_number = db.Column(db.String(50))
    bio = db.Column(db.Text)
    issues_resolved = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    is_available = db.Column(db.Boolean, default=True)
    service_areas = db.Column(db.Text)  # Comma-separated districts

    user = db.relationship('User', backref=db.backref('expert_profile', uselist=False))

    def __repr__(self):
        return f'<ExpertProfile user_id={self.user_id} area={self.expertise_area}>'


class NGOProfile(db.Model):
    """Extended profile for NGOs."""
    __tablename__ = 'ngo_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    organization_name = db.Column(db.String(200), nullable=False)
    registration_number = db.Column(db.String(100))
    focus_areas = db.Column(db.Text)  # Comma-separated
    service_districts = db.Column(db.Text)  # Comma-separated
    website = db.Column(db.String(300))
    description = db.Column(db.Text)
    established_year = db.Column(db.Integer)
    team_size = db.Column(db.Integer)
    issues_handled = db.Column(db.Integer, default=0)
    issues_completed = db.Column(db.Integer, default=0)
    is_verified = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('ngo_profile', uselist=False))

    def __repr__(self):
        return f'<NGOProfile org={self.organization_name}>'


class VolunteerProfile(db.Model):
    """Extended profile for volunteers."""
    __tablename__ = 'volunteer_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    skills = db.Column(db.Text)  # Comma-separated
    availability = db.Column(db.String(50))  # Weekdays, Weekends, Anytime
    service_areas = db.Column(db.Text)  # Comma-separated districts
    experience = db.Column(db.Text)
    tasks_completed = db.Column(db.Integer, default=0)
    hours_contributed = db.Column(db.Float, default=0.0)
    is_available = db.Column(db.Boolean, default=True)
    preferred_categories = db.Column(db.Text)  # Comma-separated

    user = db.relationship('User', backref=db.backref('volunteer_profile', uselist=False))

    def __repr__(self):
        return f'<VolunteerProfile user_id={self.user_id}>'
