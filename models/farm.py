"""
NAGARAM — Farm & Agriculture Models
Farm records, crops, soil, harvest, documents, and inputs.
"""
from datetime import datetime, timezone
from app.extensions import db


class Farm(db.Model):
    """Farm records for farmers."""
    __tablename__ = 'farms'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer_profiles.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(300))
    district = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(10))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    area_acres = db.Column(db.Float)
    land_type = db.Column(db.String(50))  # Irrigated, Rain-fed, Mixed
    soil_type = db.Column(db.String(50))
    water_source = db.Column(db.String(100))  # Well, Canal, Rain, Borewell
    irrigation_type = db.Column(db.String(50))  # Drip, Sprinkler, Flood, None
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    crops = db.relationship('Crop', backref='farm', lazy='dynamic')
    soil_records = db.relationship('SoilRecord', backref='farm', lazy='dynamic')
    harvest_records = db.relationship('HarvestRecord', backref='farm', lazy='dynamic')
    issues = db.relationship('Issue', backref='farm', lazy='dynamic')

    def __repr__(self):
        return f'<Farm {self.name}>'


class Crop(db.Model):
    """Crop records for farms."""
    __tablename__ = 'crops'

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    variety = db.Column(db.String(100))
    season = db.Column(db.String(30))  # Kharif, Rabi, Zaid
    planting_date = db.Column(db.Date)
    expected_harvest_date = db.Column(db.Date)
    actual_harvest_date = db.Column(db.Date)
    area_acres = db.Column(db.Float)
    status = db.Column(db.String(30), default='Planted')
    # Planted, Growing, Flowering, Ready for Harvest, Harvested
    expected_yield = db.Column(db.Float)  # Quintals
    actual_yield = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f'<Crop {self.name} on farm={self.farm_id}>'


class SoilRecord(db.Model):
    """Soil test records."""
    __tablename__ = 'soil_records'

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    test_date = db.Column(db.Date, nullable=False)
    soil_type = db.Column(db.String(50))
    ph = db.Column(db.Float)
    nitrogen = db.Column(db.Float)  # kg/ha
    phosphorus = db.Column(db.Float)  # kg/ha
    potassium = db.Column(db.Float)  # kg/ha
    organic_carbon = db.Column(db.Float)  # %
    organic_matter = db.Column(db.Float)  # %
    moisture = db.Column(db.Float)  # %
    ec = db.Column(db.Float)  # Electrical conductivity dS/m
    lab_name = db.Column(db.String(200))
    recommendations = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f'<SoilRecord farm={self.farm_id} date={self.test_date}>'


class HarvestRecord(db.Model):
    """Harvest records."""
    __tablename__ = 'harvest_records'

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    harvest_date = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Float)  # Quintals
    quality_grade = db.Column(db.String(10))  # A, B, C
    storage_location = db.Column(db.String(200))
    storage_type = db.Column(db.String(50))  # Warehouse, Cold Storage, Home
    expected_shelf_life_days = db.Column(db.Integer)
    selling_price = db.Column(db.Float)
    buyer = db.Column(db.String(200))
    sold_date = db.Column(db.Date)
    sold_quantity = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f'<HarvestRecord {self.crop_name} {self.harvest_date}>'


class FarmDocument(db.Model):
    """Farm documents (land records, certificates, etc.)."""
    __tablename__ = 'farm_documents'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer_profiles.id'), nullable=False)
    farmer = db.relationship('FarmerProfile', backref='documents')
    document_type = db.Column(db.String(50), nullable=False)
    # land_record, soil_report, insurance, subsidy, license, other
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(500))
    file_name = db.Column(db.String(300))
    issue_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f'<FarmDocument {self.title}>'


class FarmInput(db.Model):
    """Agricultural input records (seeds, fertilizers, pesticides)."""
    __tablename__ = 'farm_inputs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    input_type = db.Column(db.String(50), nullable=False)
    # seed, fertilizer, pesticide, herbicide, equipment, other
    brand = db.Column(db.String(100))
    supplier = db.Column(db.String(200))
    unit = db.Column(db.String(20))  # kg, litre, piece
    price = db.Column(db.Float)
    quantity_available = db.Column(db.Float)
    description = db.Column(db.Text)
    suitable_crops = db.Column(db.Text)  # Comma-separated
    rating = db.Column(db.Float, default=0.0)
    is_organic = db.Column(db.Boolean, default=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f'<FarmInput {self.name} ({self.input_type})>'
