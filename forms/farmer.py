"""
NAGARAM — Farmer Module Forms
Forms for all farmer portal modules.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, TextAreaField, SelectField, FloatField,
    IntegerField, DateField, SubmitField, BooleanField
)
from wtforms.validators import DataRequired, Length, Optional, NumberRange


class FarmForm(FlaskForm):
    """Form for creating/editing farms."""
    name = StringField('Farm Name', validators=[
        DataRequired(), Length(max=200)
    ])
    location = StringField('Location', validators=[Optional(), Length(max=300)])
    district = StringField('District', validators=[Optional(), Length(max=100)])
    state = StringField('State', validators=[Optional(), Length(max=100)])
    pincode = StringField('Pincode', validators=[Optional(), Length(max=10)])
    area_acres = FloatField('Area (Acres)', validators=[
        Optional(), NumberRange(min=0)
    ])
    land_type = SelectField('Land Type', choices=[
        ('', 'Select'),
        ('Irrigated', 'Irrigated'),
        ('Rain-fed', 'Rain-fed'),
        ('Mixed', 'Mixed'),
    ], validators=[Optional()])
    soil_type = SelectField('Soil Type', choices=[
        ('', 'Select'),
        ('Alluvial', 'Alluvial'),
        ('Black (Regur)', 'Black (Regur)'),
        ('Red', 'Red'),
        ('Laterite', 'Laterite'),
        ('Sandy', 'Sandy'),
        ('Clay', 'Clay'),
        ('Loamy', 'Loamy'),
        ('Sandy Loam', 'Sandy Loam'),
        ('Clay Loam', 'Clay Loam'),
        ('Other', 'Other'),
    ], validators=[Optional()])
    water_source = SelectField('Water Source', choices=[
        ('', 'Select'),
        ('Well', 'Well'),
        ('Borewell', 'Borewell'),
        ('Canal', 'Canal'),
        ('River', 'River'),
        ('Rain', 'Rain'),
        ('Tank/Pond', 'Tank/Pond'),
        ('Multiple', 'Multiple'),
    ], validators=[Optional()])
    irrigation_type = SelectField('Irrigation Type', choices=[
        ('', 'Select'),
        ('Drip', 'Drip'),
        ('Sprinkler', 'Sprinkler'),
        ('Flood', 'Flood / Surface'),
        ('Furrow', 'Furrow'),
        ('None', 'Rain-fed Only'),
    ], validators=[Optional()])
    submit = SubmitField('Save Farm')


class CropForm(FlaskForm):
    """Form for crop records."""
    name = StringField('Crop Name', validators=[
        DataRequired(), Length(max=100)
    ])
    variety = StringField('Variety', validators=[Optional(), Length(max=100)])
    farm_id = SelectField('Farm', coerce=int, validators=[DataRequired()])
    season = SelectField('Season', choices=[
        ('Kharif', 'Kharif (Jun-Oct)'),
        ('Rabi', 'Rabi (Oct-Mar)'),
        ('Zaid', 'Zaid (Mar-Jun)'),
    ], validators=[DataRequired()])
    planting_date = DateField('Planting Date', validators=[Optional()])
    expected_harvest_date = DateField('Expected Harvest Date', validators=[Optional()])
    area_acres = FloatField('Area (Acres)', validators=[
        Optional(), NumberRange(min=0)
    ])
    expected_yield = FloatField('Expected Yield (Quintals)', validators=[
        Optional(), NumberRange(min=0)
    ])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=2000)])
    submit = SubmitField('Save Crop')


class SoilRecordForm(FlaskForm):
    """Form for soil test records."""
    farm_id = SelectField('Farm', coerce=int, validators=[DataRequired()])
    test_date = DateField('Test Date', validators=[DataRequired()])
    soil_type = SelectField('Soil Type', choices=[
        ('', 'Select'),
        ('Alluvial', 'Alluvial'),
        ('Black', 'Black'),
        ('Red', 'Red'),
        ('Laterite', 'Laterite'),
        ('Sandy', 'Sandy'),
        ('Clay', 'Clay'),
        ('Loamy', 'Loamy'),
    ], validators=[Optional()])
    ph = FloatField('pH', validators=[Optional(), NumberRange(min=0, max=14)])
    nitrogen = FloatField('Nitrogen (kg/ha)', validators=[
        Optional(), NumberRange(min=0)
    ])
    phosphorus = FloatField('Phosphorus (kg/ha)', validators=[
        Optional(), NumberRange(min=0)
    ])
    potassium = FloatField('Potassium (kg/ha)', validators=[
        Optional(), NumberRange(min=0)
    ])
    organic_carbon = FloatField('Organic Carbon (%)', validators=[
        Optional(), NumberRange(min=0, max=100)
    ])
    organic_matter = FloatField('Organic Matter (%)', validators=[
        Optional(), NumberRange(min=0, max=100)
    ])
    moisture = FloatField('Moisture (%)', validators=[
        Optional(), NumberRange(min=0, max=100)
    ])
    lab_name = StringField('Lab Name', validators=[Optional(), Length(max=200)])
    recommendations = TextAreaField('Recommendations', validators=[
        Optional(), Length(max=3000)
    ])
    submit = SubmitField('Save Record')


class HarvestForm(FlaskForm):
    """Form for harvest records."""
    farm_id = SelectField('Farm', coerce=int, validators=[DataRequired()])
    crop_name = StringField('Crop', validators=[DataRequired(), Length(max=100)])
    harvest_date = DateField('Harvest Date', validators=[DataRequired()])
    quantity = FloatField('Quantity (Quintals)', validators=[
        Optional(), NumberRange(min=0)
    ])
    quality_grade = SelectField('Quality Grade', choices=[
        ('', 'Select'),
        ('A', 'Grade A'),
        ('B', 'Grade B'),
        ('C', 'Grade C'),
    ], validators=[Optional()])
    storage_location = StringField('Storage Location', validators=[
        Optional(), Length(max=200)
    ])
    storage_type = SelectField('Storage Type', choices=[
        ('', 'Select'),
        ('Warehouse', 'Warehouse'),
        ('Cold Storage', 'Cold Storage'),
        ('Home', 'Home Storage'),
        ('Open', 'Open Storage'),
    ], validators=[Optional()])
    expected_shelf_life_days = IntegerField('Expected Shelf Life (Days)', validators=[
        Optional(), NumberRange(min=0)
    ])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=2000)])
    submit = SubmitField('Save Record')


class TransportRequestForm(FlaskForm):
    """Form for transport finder."""
    pickup_location = StringField('Pickup Location', validators=[
        DataRequired(), Length(max=300)
    ])
    destination = StringField('Destination', validators=[
        DataRequired(), Length(max=300)
    ])
    crop_name = StringField('Crop / Load', validators=[
        DataRequired(), Length(max=100)
    ])
    quantity = FloatField('Quantity (Tonnes)', validators=[
        Optional(), NumberRange(min=0)
    ])
    vehicle_type = SelectField('Preferred Vehicle', choices=[
        ('', 'Any'),
        ('Truck', 'Truck'),
        ('Mini-truck', 'Mini-truck'),
        ('Tractor-trolley', 'Tractor-trolley'),
        ('Pickup', 'Pickup'),
        ('Tempo', 'Tempo'),
    ], validators=[Optional()])
    needs_refrigeration = BooleanField('Needs Refrigeration')
    preferred_date = DateField('Preferred Date', validators=[Optional()])
    submit = SubmitField('Find Transport')


class BuyerListingForm(FlaskForm):
    """Form for farmer crop listings."""
    crop_name = StringField('Crop Name', validators=[
        DataRequired(), Length(max=100)
    ])
    variety = StringField('Variety', validators=[Optional(), Length(max=100)])
    quantity = FloatField('Quantity (Quintals)', validators=[
        DataRequired(), NumberRange(min=0.1)
    ])
    expected_price = FloatField('Expected Price (₹/Quintal)', validators=[
        Optional(), NumberRange(min=0)
    ])
    quality_grade = SelectField('Quality', choices=[
        ('A', 'Grade A'),
        ('B', 'Grade B'),
        ('C', 'Grade C'),
    ], validators=[Optional()])
    location = StringField('Location', validators=[
        Optional(), Length(max=300)
    ])
    district = StringField('District', validators=[Optional(), Length(max=100)])
    harvest_date = DateField('Harvest Date', validators=[Optional()])
    available_from = DateField('Available From', validators=[Optional()])
    description = TextAreaField('Description', validators=[
        Optional(), Length(max=2000)
    ])
    submit = SubmitField('Create Listing')


class ConsultationForm(FlaskForm):
    """Form for requesting expert consultation."""
    category = SelectField('Category', choices=[
        ('crop', 'Crop Issue'),
        ('soil', 'Soil Problem'),
        ('irrigation', 'Irrigation'),
        ('pest_disease', 'Pest / Disease'),
        ('market', 'Market Query'),
        ('general', 'General Question'),
    ], validators=[DataRequired()])
    crop_name = StringField('Related Crop', validators=[
        Optional(), Length(max=100)
    ])
    subject = StringField('Subject', validators=[
        DataRequired(), Length(min=5, max=300)
    ])
    question = TextAreaField('Your Question', validators=[
        DataRequired(), Length(min=10, max=5000)
    ])
    submit = SubmitField('Ask Expert')


class CropRecommendationForm(FlaskForm):
    """Form for crop recommendation engine."""
    location = StringField('Location', validators=[
        DataRequired(), Length(max=200)
    ])
    soil_type = SelectField('Soil Type', choices=[
        ('Alluvial', 'Alluvial'),
        ('Black', 'Black (Regur)'),
        ('Red', 'Red'),
        ('Laterite', 'Laterite'),
        ('Sandy', 'Sandy'),
        ('Clay', 'Clay'),
        ('Loamy', 'Loamy'),
        ('Sandy Loam', 'Sandy Loam'),
        ('Clay Loam', 'Clay Loam'),
    ], validators=[DataRequired()])
    season = SelectField('Season', choices=[
        ('Kharif', 'Kharif (Jun-Oct)'),
        ('Rabi', 'Rabi (Oct-Mar)'),
        ('Zaid', 'Zaid (Mar-Jun)'),
    ], validators=[DataRequired()])
    water_availability = SelectField('Water Availability', choices=[
        ('High', 'High (Irrigated)'),
        ('Medium', 'Medium'),
        ('Low', 'Low (Rain-fed)'),
    ], validators=[DataRequired()])
    ph = FloatField('Soil pH (if known)', validators=[
        Optional(), NumberRange(min=0, max=14)
    ])
    previous_crop = StringField('Previous Crop', validators=[
        Optional(), Length(max=100)
    ])
    submit = SubmitField('Get Recommendations')
