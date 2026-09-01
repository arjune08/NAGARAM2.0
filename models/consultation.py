"""
NAGARAM — Consultation Model
Expert consultations linking farmers to agricultural experts.
"""
from datetime import datetime, timezone
from app.extensions import db


class Consultation(db.Model):
    """Expert consultation records."""
    __tablename__ = 'consultations'

    id = db.Column(db.Integer, primary_key=True)
    consultation_id = db.Column(db.String(20), unique=True, nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer_profiles.id'), nullable=False)
    farmer = db.relationship('FarmerProfile', backref='consultations')
    expert_id = db.Column(db.Integer, db.ForeignKey('expert_profiles.id'))
    expert = db.relationship('ExpertProfile', backref='consultations')

    category = db.Column(db.String(50), nullable=False)
    # crop, soil, irrigation, pest_disease, market, general
    crop_name = db.Column(db.String(100))
    subject = db.Column(db.String(300), nullable=False)
    question = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)

    # Expert response
    diagnosis = db.Column(db.Text)
    recommendation = db.Column(db.Text)
    expert_notes = db.Column(db.Text)

    # Status
    status = db.Column(db.String(30), default='Pending')
    # Pending, Assigned, In Review, Answered, Follow-up, Closed
    priority = db.Column(db.String(20), default='Medium')

    # Farmer feedback
    farmer_feedback = db.Column(db.Text)
    farmer_rating = db.Column(db.Integer)  # 1-5

    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    answered_at = db.Column(db.DateTime)
    closed_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Consultation {self.consultation_id}>'
