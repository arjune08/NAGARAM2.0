"""
NAGARAM — Government Scheme Model
Government schemes with eligibility criteria.
"""
from datetime import datetime, timezone
from app.extensions import db


class GovernmentScheme(db.Model):
    """Government agricultural and civic schemes."""
    __tablename__ = 'government_schemes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    scheme_code = db.Column(db.String(50), unique=True)
    department = db.Column(db.String(200))
    scheme_type = db.Column(db.String(50))  # subsidy, insurance, loan, grant, other
    description = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.Text)
    eligibility = db.Column(db.Text)
    required_documents = db.Column(db.Text)
    application_process = db.Column(db.Text)
    application_url = db.Column(db.String(500))
    max_benefit_amount = db.Column(db.Float)
    target_group = db.Column(db.String(200))
    # small_farmer, marginal_farmer, all_farmers, women, sc_st, general
    min_land_holding = db.Column(db.Float)  # Acres
    max_land_holding = db.Column(db.Float)
    applicable_states = db.Column(db.Text)  # Comma-separated, or 'All India'
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    source = db.Column(db.String(100), default='Demo Data')
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    @classmethod
    def seed_default_schemes(cls):
        """Seed default government agricultural schemes."""
        schemes = [
            {
                'name': 'PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)',
                'scheme_code': 'PM-KISAN-01',
                'department': 'Department of Agriculture & Farmers Welfare',
                'scheme_type': 'grant',
                'description': 'Direct income support of ₹6,000 per year in three equal installments to all landholding farmer families across India.',
                'benefits': '₹6,000 per year transferred directly to bank account in 3 installments of ₹2,000.',
                'eligibility': 'All landholding farmer families with cultivable land in their name.',
                'required_documents': 'Aadhaar Card, Landholding Ownership Papers, Bank Account Details',
                'application_process': 'Apply online via PM-KISAN Portal or visit nearest Common Service Center (CSC).',
                'application_url': 'https://pmkisan.gov.in',
                'max_benefit_amount': 6000.0,
                'target_group': 'all_farmers',
                'applicable_states': 'All India',
            },
            {
                'name': 'Pradhan Mantri Fasal Bima Yojana (PMFBY)',
                'scheme_code': 'PMFBY-02',
                'department': 'Ministry of Agriculture',
                'scheme_type': 'insurance',
                'description': 'Crop insurance scheme providing financial support to farmers suffering crop loss/damage due to natural calamities.',
                'benefits': 'Comprehensive risk cover for crops against non-preventable natural risks.',
                'eligibility': 'All farmers growing notified crops in notified areas including sharecroppers and tenant farmers.',
                'required_documents': 'Land Possession Certificate, Sowing Certificate, Aadhaar, Bank Details',
                'application_process': 'Apply through bank branch, insurance company agent, or PMFBY online portal.',
                'application_url': 'https://pmfby.gov.in',
                'max_benefit_amount': 150000.0,
                'target_group': 'all_farmers',
                'applicable_states': 'All India',
            },
            {
                'name': 'Kisan Credit Card (KCC) Scheme',
                'scheme_code': 'KCC-03',
                'department': 'Reserve Bank of India & NABARD',
                'scheme_type': 'loan',
                'description': 'Concessional credit to farmers to meet crop production and post-harvest requirements.',
                'benefits': 'Credit limit up to ₹3 Lakh at 4% interest rate (with prompt repayment incentive).',
                'eligibility': 'Individual farmers, joint borrowers, tenant farmers, self-help groups.',
                'required_documents': 'Application Form, Identity Proof, Address Proof, Land Documents',
                'application_process': 'Submit application form at any commercial or regional rural bank branch.',
                'application_url': 'https://www.nabard.org',
                'max_benefit_amount': 300000.0,
                'target_group': 'all_farmers',
                'applicable_states': 'All India',
            },
            {
                'name': 'Paramparagat Krishi Vikas Yojana (PKVY)',
                'scheme_code': 'PKVY-04',
                'department': 'Department of Agriculture',
                'scheme_type': 'subsidy',
                'description': 'Promotes organic farming through cluster approach and Participatory Guarantee System (PGS) certification.',
                'benefits': '₹50,000 per hectare assistance for organic inputs, certification and marketing.',
                'eligibility': 'Farmers forming clusters of 50 or more acres for organic farming.',
                'required_documents': 'Cluster Member Agreement, Land Records, Aadhaar',
                'application_process': 'Apply through Regional Council or State Agriculture Department.',
                'application_url': 'https://pgsindia-ncof.gov.in',
                'max_benefit_amount': 50000.0,
                'target_group': 'all_farmers',
                'applicable_states': 'All India',
            },
        ]

        created = []
        for sdata in schemes:
            scheme = cls.query.filter_by(scheme_code=sdata['scheme_code']).first()
            if not scheme:
                scheme = cls(**sdata)
                db.session.add(scheme)
                created.append(scheme)

        db.session.commit()
        return created

    def __repr__(self):
        return f'<GovernmentScheme {self.name}>'
