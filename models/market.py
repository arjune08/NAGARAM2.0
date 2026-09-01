"""
NAGARAM — Market & Transport Models
Market prices, buyer listings, and transport options.
"""
from datetime import datetime, timezone
from app.extensions import db


class MarketPrice(db.Model):
    """Agricultural commodity market prices."""
    __tablename__ = 'market_prices'

    id = db.Column(db.Integer, primary_key=True)
    commodity = db.Column(db.String(100), nullable=False, index=True)
    variety = db.Column(db.String(100))
    market_name = db.Column(db.String(200), nullable=False)
    district = db.Column(db.String(100))
    state = db.Column(db.String(100))
    min_price = db.Column(db.Float)  # Rs per quintal
    max_price = db.Column(db.Float)
    modal_price = db.Column(db.Float)  # Most common price
    unit = db.Column(db.String(20), default='Quintal')
    price_date = db.Column(db.Date, nullable=False)
    source = db.Column(db.String(100), default='Demo Data')
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f'<MarketPrice {self.commodity} @ {self.market_name}>'


class BuyerListing(db.Model):
    """Farmer crop listings for direct buyer connection."""
    __tablename__ = 'buyer_listings'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer_profiles.id'), nullable=False)
    farmer = db.relationship('FarmerProfile', backref='listings')
    crop_name = db.Column(db.String(100), nullable=False)
    variety = db.Column(db.String(100))
    quantity = db.Column(db.Float, nullable=False)  # Quintals
    unit = db.Column(db.String(20), default='Quintal')
    expected_price = db.Column(db.Float)
    quality_grade = db.Column(db.String(10))
    location = db.Column(db.String(300))
    district = db.Column(db.String(100))
    harvest_date = db.Column(db.Date)
    available_from = db.Column(db.Date)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    views = db.Column(db.Integer, default=0)
    inquiries = db.Column(db.Integer, default=0)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f'<BuyerListing {self.crop_name} by farmer={self.farmer_id}>'


class TransportListing(db.Model):
    """Transport options for agricultural goods."""
    __tablename__ = 'transport_listings'

    id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String(200), nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)
    # Truck, Mini-truck, Tractor-trolley, Pickup, Tempo
    capacity = db.Column(db.Float)  # Tonnes
    service_areas = db.Column(db.Text)  # Comma-separated districts
    contact_phone = db.Column(db.String(20))
    contact_name = db.Column(db.String(100))
    price_per_km = db.Column(db.Float)
    min_charge = db.Column(db.Float)
    is_available = db.Column(db.Boolean, default=True)
    is_refrigerated = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f'<TransportListing {self.provider_name}>'
