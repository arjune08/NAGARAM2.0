"""
NAGARAM — Farmer Routes
Farmer dashboard and all agricultural modules.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.issue import Issue, IssueCategory
from app.models.farm import Farm, Crop, SoilRecord, HarvestRecord, FarmDocument, FarmInput
from app.models.market import MarketPrice, BuyerListing, TransportListing
from app.models.scheme import GovernmentScheme
from app.models.consultation import Consultation
from app.forms.issue import AgriculturalIssueForm, CommentForm
from app.forms.farmer import (
    FarmForm, CropForm, SoilRecordForm, HarvestForm,
    TransportRequestForm, BuyerListingForm, ConsultationForm,
    CropRecommendationForm
)
from app.services.issue_service import create_issue, get_issue_stats
from app.services.weather_service import get_current_weather, get_weather_forecast, get_farming_alerts, get_water_advisory
from app.services.market_service import get_market_prices, get_price_trends, get_nearby_markets
from app.services.crop_service import get_crop_recommendations
from app.services.scheme_service import get_all_schemes, check_eligibility
from app.services.notification_service import get_user_notifications
from app.utils.decorators import role_required
from app.utils.helpers import (
    get_status_class, get_priority_class, time_ago,
    generate_consultation_id
)

farmer_bp = Blueprint('farmer', __name__)


@farmer_bp.before_request
@login_required
def before_request():
    pass


# ─── Dashboard ───────────────────────────────────────────────
@farmer_bp.route('/dashboard')
@role_required('farmer')
def dashboard():
    stats = get_issue_stats(issue_type='agricultural', user_id=current_user.id)
    weather = get_current_weather(location=current_user.location)
    alerts = get_farming_alerts(location=current_user.location)
    recent_issues = Issue.query.filter_by(
        reporter_id=current_user.id, issue_type='agricultural'
    ).order_by(Issue.created_at.desc()).limit(3).all()
    market = get_market_prices()
    notifications = get_user_notifications(current_user.id, limit=5)

    profile = current_user.farmer_profile
    farms = Farm.query.filter_by(farmer_id=profile.id).all() if profile else []

    return render_template('farmer/dashboard.html',
                           stats=stats, weather=weather, alerts=alerts,
                           recent_issues=recent_issues, market=market,
                           notifications=notifications, farms=farms,
                           get_status_class=get_status_class,
                           time_ago=time_ago)


# ─── Weather Intelligence ────────────────────────────────────
@farmer_bp.route('/weather')
@role_required('farmer')
def weather():
    current = get_current_weather(location=current_user.location)
    forecast = get_weather_forecast(location=current_user.location)
    alerts = get_farming_alerts(location=current_user.location)
    return render_template('farmer/weather.html',
                           current=current, forecast=forecast, alerts=alerts)


# ─── Water Advisory ──────────────────────────────────────────
@farmer_bp.route('/water-advisory')
@role_required('farmer')
def water_advisory():
    advisory = get_water_advisory(location=current_user.location)
    return render_template('farmer/water_advisory.html', advisory=advisory)


# ─── Crop Health Monitor ─────────────────────────────────────
@farmer_bp.route('/crop-health')
@role_required('farmer')
def crop_health():
    profile = current_user.farmer_profile
    issues = Issue.query.filter_by(
        reporter_id=current_user.id, issue_type='agricultural'
    ).order_by(Issue.created_at.desc()).limit(10).all()
    return render_template('farmer/crop_health.html',
                           issues=issues, get_status_class=get_status_class,
                           time_ago=time_ago)


# ─── Market Intelligence ─────────────────────────────────────
@farmer_bp.route('/market')
@role_required('farmer')
def market():
    commodity = request.args.get('commodity', '')
    prices = get_market_prices(commodity=commodity)
    trends = get_price_trends(commodity=commodity or 'Rice (Paddy)')
    markets = get_nearby_markets(district=current_user.district)
    return render_template('farmer/market.html',
                           prices=prices, trends=trends, markets=markets,
                           selected_commodity=commodity)


# ─── Digital Agriculture Advisor ──────────────────────────────
@farmer_bp.route('/advisor', methods=['GET', 'POST'])
@role_required('farmer')
def advisor():
    form = ConsultationForm()
    profile = current_user.farmer_profile

    if form.validate_on_submit() and profile:
        consultation = Consultation(
            consultation_id=generate_consultation_id(),
            farmer_id=profile.id,
            category=form.category.data,
            crop_name=form.crop_name.data,
            subject=form.subject.data,
            question=form.question.data,
        )
        db.session.add(consultation)
        db.session.commit()
        flash(f'Consultation {consultation.consultation_id} submitted. An expert will review it.', 'success')
        return redirect(url_for('farmer.advisor'))

    consultations = []
    if profile:
        consultations = Consultation.query.filter_by(
            farmer_id=profile.id
        ).order_by(Consultation.created_at.desc()).limit(10).all()

    return render_template('farmer/advisor.html',
                           form=form, consultations=consultations,
                           time_ago=time_ago)


# ─── Soil Health ─────────────────────────────────────────────
@farmer_bp.route('/soil', methods=['GET', 'POST'])
@role_required('farmer')
def soil():
    profile = current_user.farmer_profile
    form = SoilRecordForm()
    farms = Farm.query.filter_by(farmer_id=profile.id).all() if profile else []
    form.farm_id.choices = [(f.id, f.name) for f in farms]

    if form.validate_on_submit():
        record = SoilRecord(
            farm_id=form.farm_id.data,
            test_date=form.test_date.data,
            soil_type=form.soil_type.data,
            ph=form.ph.data,
            nitrogen=form.nitrogen.data,
            phosphorus=form.phosphorus.data,
            potassium=form.potassium.data,
            organic_carbon=form.organic_carbon.data,
            organic_matter=form.organic_matter.data,
            moisture=form.moisture.data,
            lab_name=form.lab_name.data,
            recommendations=form.recommendations.data,
        )
        db.session.add(record)
        db.session.commit()
        flash('Soil record saved.', 'success')
        return redirect(url_for('farmer.soil'))

    records = []
    if farms:
        farm_ids = [f.id for f in farms]
        records = SoilRecord.query.filter(
            SoilRecord.farm_id.in_(farm_ids)
        ).order_by(SoilRecord.test_date.desc()).all()

    return render_template('farmer/soil.html',
                           form=form, records=records, farms=farms)


# ─── Crop Recommendation ────────────────────────────────────
@farmer_bp.route('/crop-recommendation', methods=['GET', 'POST'])
@role_required('farmer')
def crop_recommendation():
    form = CropRecommendationForm()
    recommendations = None

    if form.validate_on_submit():
        recommendations = get_crop_recommendations(
            soil_type=form.soil_type.data,
            season=form.season.data,
            water_availability=form.water_availability.data,
            ph=form.ph.data,
            previous_crop=form.previous_crop.data,
            location=form.location.data,
        )

    return render_template('farmer/crop_recommendation.html',
                           form=form, recommendations=recommendations)


# ─── Post-Harvest Manager ───────────────────────────────────
@farmer_bp.route('/post-harvest', methods=['GET', 'POST'])
@role_required('farmer')
def post_harvest():
    profile = current_user.farmer_profile
    form = HarvestForm()
    farms = Farm.query.filter_by(farmer_id=profile.id).all() if profile else []
    form.farm_id.choices = [(f.id, f.name) for f in farms]

    if form.validate_on_submit():
        record = HarvestRecord(
            farm_id=form.farm_id.data,
            crop_name=form.crop_name.data,
            harvest_date=form.harvest_date.data,
            quantity=form.quantity.data,
            quality_grade=form.quality_grade.data,
            storage_location=form.storage_location.data,
            storage_type=form.storage_type.data,
            expected_shelf_life_days=form.expected_shelf_life_days.data,
            notes=form.notes.data,
        )
        db.session.add(record)
        db.session.commit()
        flash('Harvest record saved.', 'success')
        return redirect(url_for('farmer.post_harvest'))

    records = []
    if farms:
        farm_ids = [f.id for f in farms]
        records = HarvestRecord.query.filter(
            HarvestRecord.farm_id.in_(farm_ids)
        ).order_by(HarvestRecord.harvest_date.desc()).all()

    return render_template('farmer/post_harvest.html',
                           form=form, records=records, farms=farms)


# ─── Transport Finder ───────────────────────────────────────
@farmer_bp.route('/transport', methods=['GET', 'POST'])
@role_required('farmer')
def transport():
    form = TransportRequestForm()
    transports = TransportListing.query.filter_by(
        is_available=True
    ).order_by(TransportListing.rating.desc()).all()

    return render_template('farmer/transport.html',
                           form=form, transports=transports)


# ─── Government Schemes ─────────────────────────────────────
@farmer_bp.route('/schemes')
@role_required('farmer')
def schemes():
    profile = current_user.farmer_profile
    land_holding = profile.land_holding if profile else None
    result = check_eligibility(
        land_holding=land_holding,
        state=current_user.state,
    )
    all_schemes = get_all_schemes()
    return render_template('farmer/schemes.html',
                           result=result, all_schemes=all_schemes)


# ─── Farm Records ───────────────────────────────────────────
@farmer_bp.route('/farm-records', methods=['GET', 'POST'])
@role_required('farmer')
def farm_records():
    profile = current_user.farmer_profile
    farm_form = FarmForm()
    crop_form = CropForm()

    farms = Farm.query.filter_by(farmer_id=profile.id).all() if profile else []
    crop_form.farm_id.choices = [(f.id, f.name) for f in farms]

    return render_template('farmer/farm_records.html',
                           farm_form=farm_form, crop_form=crop_form,
                           farms=farms)


@farmer_bp.route('/farm-records/add-farm', methods=['POST'])
@role_required('farmer')
def add_farm():
    profile = current_user.farmer_profile
    form = FarmForm()

    if form.validate_on_submit() and profile:
        farm = Farm(
            farmer_id=profile.id,
            name=form.name.data,
            location=form.location.data,
            district=form.district.data,
            state=form.state.data,
            pincode=form.pincode.data,
            area_acres=form.area_acres.data,
            land_type=form.land_type.data,
            soil_type=form.soil_type.data,
            water_source=form.water_source.data,
            irrigation_type=form.irrigation_type.data,
        )
        db.session.add(farm)
        db.session.commit()
        flash('Farm added successfully.', 'success')
    else:
        flash('Please check the form and try again.', 'error')

    return redirect(url_for('farmer.farm_records'))


@farmer_bp.route('/farm-records/add-crop', methods=['POST'])
@role_required('farmer')
def add_crop():
    profile = current_user.farmer_profile
    farms = Farm.query.filter_by(farmer_id=profile.id).all() if profile else []
    form = CropForm()
    form.farm_id.choices = [(f.id, f.name) for f in farms]

    if form.validate_on_submit():
        crop = Crop(
            farm_id=form.farm_id.data,
            name=form.name.data,
            variety=form.variety.data,
            season=form.season.data,
            planting_date=form.planting_date.data,
            expected_harvest_date=form.expected_harvest_date.data,
            area_acres=form.area_acres.data,
            expected_yield=form.expected_yield.data,
            notes=form.notes.data,
        )
        db.session.add(crop)
        db.session.commit()
        flash('Crop record added.', 'success')
    else:
        flash('Please check the form and try again.', 'error')

    return redirect(url_for('farmer.farm_records'))


# ─── Input Marketplace ──────────────────────────────────────
@farmer_bp.route('/marketplace')
@role_required('farmer')
def marketplace():
    input_type = request.args.get('type', '')
    query = FarmInput.query
    if input_type:
        query = query.filter_by(input_type=input_type)
    inputs = query.order_by(FarmInput.name).all()
    return render_template('farmer/marketplace.html',
                           inputs=inputs, selected_type=input_type)


# ─── Buyer Connection ───────────────────────────────────────
@farmer_bp.route('/buyer-connection', methods=['GET', 'POST'])
@role_required('farmer')
def buyer_connection():
    profile = current_user.farmer_profile
    form = BuyerListingForm()

    if form.validate_on_submit() and profile:
        listing = BuyerListing(
            farmer_id=profile.id,
            crop_name=form.crop_name.data,
            variety=form.variety.data,
            quantity=form.quantity.data,
            expected_price=form.expected_price.data,
            quality_grade=form.quality_grade.data,
            location=form.location.data or current_user.location,
            district=form.district.data or current_user.district,
            harvest_date=form.harvest_date.data,
            available_from=form.available_from.data,
            description=form.description.data,
        )
        db.session.add(listing)
        db.session.commit()
        flash('Listing created successfully.', 'success')
        return redirect(url_for('farmer.buyer_connection'))

    my_listings = []
    all_listings = BuyerListing.query.filter_by(is_active=True).order_by(
        BuyerListing.created_at.desc()
    ).limit(20).all()
    if profile:
        my_listings = BuyerListing.query.filter_by(
            farmer_id=profile.id
        ).order_by(BuyerListing.created_at.desc()).all()

    return render_template('farmer/buyer_connection.html',
                           form=form, my_listings=my_listings,
                           all_listings=all_listings, time_ago=time_ago)


# ─── Report Agricultural Issue ──────────────────────────────
@farmer_bp.route('/report-issue', methods=['GET', 'POST'])
@role_required('farmer')
def report_issue():
    form = AgriculturalIssueForm()
    categories = IssueCategory.query.filter_by(
        issue_type='agricultural', is_active=True
    ).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]

    profile = current_user.farmer_profile
    farms = Farm.query.filter_by(farmer_id=profile.id).all() if profile else []
    form.farm_id.choices = [(0, 'Select Farm')] + [(f.id, f.name) for f in farms]

    if form.validate_on_submit():
        form_data = {
            'title': form.title.data,
            'description': form.description.data,
            'category_id': form.category_id.data,
            'location': form.location.data,
            'district': form.district.data,
            'latitude': form.latitude.data,
            'longitude': form.longitude.data,
            'priority': form.priority.data,
            'crop_name': form.crop_name.data,
            'affected_area': form.affected_area.data,
            'farm_id': form.farm_id.data if form.farm_id.data else None,
        }
        images = request.files.getlist('images')
        issue = create_issue(form_data, current_user, 'agricultural', images)
        flash(f'Issue {issue.issue_id} submitted successfully.', 'success')
        return redirect(url_for('farmer.crop_health'))

    return render_template('farmer/report_issue.html', form=form)


# ─── Notifications ──────────────────────────────────────────
@farmer_bp.route('/notifications')
@role_required('farmer')
def notifications():
    notifs = get_user_notifications(current_user.id, limit=50)
    return render_template('farmer/notifications.html',
                           notifications=notifs, time_ago=time_ago)


# ─── Profile ────────────────────────────────────────────────
@farmer_bp.route('/profile')
@role_required('farmer')
def profile():
    stats = get_issue_stats(issue_type='agricultural', user_id=current_user.id)
    farmer_profile = current_user.farmer_profile
    farms = Farm.query.filter_by(farmer_id=farmer_profile.id).all() if farmer_profile else []
    return render_template('farmer/profile.html',
                           stats=stats, farms=farms)
