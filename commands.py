"""
NAGARAM — CLI Commands & Database Seeder
Seed demo data for instant platform demo and testing.
"""
from datetime import datetime, timezone
import click
from flask.cli import AppGroup
from app.extensions import db
from app.models.user import User, Role
from app.models.profile import (
    CitizenProfile, FarmerProfile, ExpertProfile,
    NGOProfile, VolunteerProfile
)
from app.models.issue import IssueCategory, Issue, IssueUpdate, IssueComment
from app.models.scheme import GovernmentScheme
from app.models.market import MarketPrice, BuyerListing, TransportListing
from app.models.farm import Farm, Crop, SoilRecord, HarvestRecord, FarmInput
from app.models.consultation import Consultation
from app.models.notification import Notification

seed_cli = AppGroup('seed', help='Database seed commands.')


@seed_cli.command('init-db')
def init_db():
    """Create all database tables."""
    db.create_all()
    click.echo('Database tables created successfully.')


@seed_cli.command('demo-data')
def seed_demo_data():
    """Seed complete demo data including users, categories, schemes, and issues."""
    click.echo('Seeding database with demo data...')

    # 1. Create Roles
    roles = Role.seed_default_roles()
    click.echo('Roles seeded.')

    # 2. Create Issue Categories
    IssueCategory.seed_default_categories()
    click.echo('Categories seeded.')

    # 3. Create Government Schemes
    GovernmentScheme.seed_default_schemes()
    click.echo('Government schemes seeded.')

    # 4. Create Demo Users (password: demo123)
    demo_users_data = [
        {
            'username': 'admin',
            'email': 'admin@nagaram.gov.in',
            'full_name': 'System Administrator',
            'role_name': 'admin',
            'phone': '9876543210',
            'location': 'New Delhi',
            'district': 'Central Delhi',
            'state': 'Delhi',
        },
        {
            'username': 'citizen1',
            'email': 'citizen@nagaram.gov.in',
            'full_name': 'Rajesh Kumar',
            'role_name': 'citizen',
            'phone': '9876543211',
            'location': 'Connaught Place',
            'district': 'Central Delhi',
            'state': 'Delhi',
        },
        {
            'username': 'farmer1',
            'email': 'farmer@nagaram.gov.in',
            'full_name': 'Ramesh Singh',
            'role_name': 'farmer',
            'phone': '9876543212',
            'location': 'Karnal',
            'district': 'Karnal',
            'state': 'Haryana',
        },
        {
            'username': 'expert1',
            'email': 'expert@nagaram.gov.in',
            'full_name': 'Dr. Anita Sharma',
            'role_name': 'expert',
            'phone': '9876543213',
            'location': 'Pusa',
            'district': 'New Delhi',
            'state': 'Delhi',
        },
        {
            'username': 'ngo1',
            'email': 'ngo@nagaram.gov.in',
            'full_name': 'Jan Seva Foundation',
            'role_name': 'ngo',
            'phone': '9876543214',
            'location': 'Jaipur',
            'district': 'Jaipur',
            'state': 'Rajasthan',
        },
        {
            'username': 'volunteer1',
            'email': 'volunteer@nagaram.gov.in',
            'full_name': 'Suresh Patel',
            'role_name': 'volunteer',
            'phone': '9876543215',
            'location': 'Ahmedabad',
            'district': 'Ahmedabad',
            'state': 'Gujarat',
        },
    ]

    users_by_role = {}
    for udata in demo_users_data:
        existing = User.query.filter_by(email=udata['email']).first()
        if not existing:
            role = Role.query.filter_by(name=udata['role_name']).first()
            user = User(
                username=udata['username'],
                email=udata['email'],
                full_name=udata['full_name'],
                role_id=role.id,
                phone=udata['phone'],
                location=udata['location'],
                district=udata['district'],
                state=udata['state'],
            )
            user.set_password('demo123')
            db.session.add(user)
            db.session.flush()

            # Create specific profiles
            if udata['role_name'] == 'citizen':
                db.session.add(CitizenProfile(user_id=user.id))
            elif udata['role_name'] == 'farmer':
                db.session.add(FarmerProfile(
                    user_id=user.id,
                    farming_type='Organic',
                    land_holding=5.5,
                    primary_crop='Rice (Paddy)',
                    secondary_crops='Wheat, Sugarcane',
                ))
            elif udata['role_name'] == 'expert':
                db.session.add(ExpertProfile(
                    user_id=user.id,
                    expertise_area='Crop Pathology',
                    specialization='Pest & Disease Management',
                    qualification='Ph.D in Agronomy',
                    experience_years=12,
                    institution='Indian Agricultural Research Institute',
                ))
            elif udata['role_name'] == 'ngo':
                db.session.add(NGOProfile(
                    user_id=user.id,
                    organization_name='Jan Seva Foundation',
                    registration_number='NGO-2020-8849',
                    focus_areas='Rural Infrastructure, Water Harvesting',
                    service_districts='Jaipur, Alwar, Dausa',
                ))
            elif udata['role_name'] == 'volunteer':
                db.session.add(VolunteerProfile(
                    user_id=user.id,
                    skills='First Aid, Survey, Community Outreach',
                    availability='Weekends',
                ))
            users_by_role[udata['role_name']] = user
        else:
            users_by_role[udata['role_name']] = existing

    db.session.commit()
    click.echo('Demo users created (password: demo123).')

    # 5. Create Sample Farm & Crops
    farmer_user = users_by_role.get('farmer')
    if farmer_user and farmer_user.farmer_profile:
        farm = Farm.query.filter_by(farmer_id=farmer_user.farmer_profile.id).first()
        if not farm:
            farm = Farm(
                farmer_id=farmer_user.farmer_profile.id,
                name='Green Acres Farm',
                location='Sector 14, Karnal',
                district='Karnal',
                state='Haryana',
                pincode='132001',
                area_acres=5.5,
                land_type='Agricultural',
                soil_type='Alluvial',
                water_source='Borewell',
                irrigation_type='Drip',
            )
            db.session.add(farm)
            db.session.flush()

            crop1 = Crop(
                farm_id=farm.id,
                name='Rice (Paddy)',
                variety='Basmati 1121',
                season='Kharif',
                area_acres=3.0,
                expected_yield=45.0,
            )
            crop2 = Crop(
                farm_id=farm.id,
                name='Wheat',
                variety='HD-2967',
                season='Rabi',
                area_acres=2.5,
                expected_yield=50.0,
            )
            db.session.add_all([crop1, crop2])
            db.session.commit()
            click.echo('Demo farm and crops created.')

    # 6. Create Demo Issues
    citizen_user = users_by_role.get('citizen')
    expert_user = users_by_role.get('expert')
    ngo_user = users_by_role.get('ngo')

    if citizen_user:
        civic_cat = IssueCategory.query.filter_by(issue_type='civic').first()
        if civic_cat and not Issue.query.filter_by(reporter_id=citizen_user.id).first():
            issue1 = Issue(
                issue_id='CIV-2026-0001',
                reporter_id=citizen_user.id,
                reporter_type=citizen_user.role_name,
                issue_type='civic',
                category_id=civic_cat.id,
                title='Broken Streetlight causing safety hazard',
                description='The main street light on Sector 4 road has been flickering and completely turned off for the last 5 days.',
                location='Sector 4, Main Market Road',
                district='Central Delhi',
                state='Delhi',
                priority='Medium',
                status='Submitted',
            )
            db.session.add(issue1)

    if farmer_user:
        agri_cat = IssueCategory.query.filter_by(issue_type='agricultural').first()
        if agri_cat and not Issue.query.filter_by(reporter_id=farmer_user.id).first():
            issue2 = Issue(
                issue_id='AGR-2026-0001',
                reporter_id=farmer_user.id,
                reporter_type=farmer_user.role_name,
                issue_type='agricultural',
                category_id=agri_cat.id,
                title='Yellowing leaves on Basmati Paddy crop',
                description='Upper leaves are showing yellow stripes and drying from tips. Affected area is around 1.5 acres.',
                location='Karnal Farm #2',
                district='Karnal',
                state='Haryana',
                priority='High',
                status='In Progress',
                assigned_to_id=expert_user.id if expert_user else None,
                crop_name='Rice (Paddy)',
                affected_area=1.5,
            )
            db.session.add(issue2)

    # 7. Create Farm Inputs
    if not FarmInput.query.first():
        inputs = [
            FarmInput(name='Neem Oil 1500 PPM', input_type='pesticide', brand='KisanCare', price=450, unit='Litre', supplier='AgriStore Karnal', is_organic=True, description='Bio-pesticide for insect pest control'),
            FarmInput(name='N P K 19:19:19 Water Soluble', input_type='fertilizer', brand='Iffco', price=120, unit='Kg', supplier='Iffco Kendra', is_organic=False, description='Balanced plant nutrition fertilizer'),
            FarmInput(name='Basmati Paddy Seeds 1121', input_type='seed', brand='Pusa Seeds', price=85, unit='Kg', supplier='State Seed Corp', is_organic=False, description='Certified high yield paddy seed'),
            FarmInput(name='Solar Water Pump 5HP', input_type='equipment', brand='Tata Power Solar', price=125000, unit='Piece', supplier='Tata Solar Dealer', is_organic=False, description='Submersible solar pump with 5yr warranty'),
        ]
        db.session.add_all(inputs)

    # 8. Create Transport Listings
    if not TransportListing.query.first():
        transports = [
            TransportListing(provider_name='Haryana Goods Carrier', vehicle_type='Eicher 14ft Truck', capacity=5.0, price_per_km=35.0, contact_phone='9812345678', service_areas='Karnal, Panipat, Kurukshetra', is_refrigerated=False, rating=4.8),
            TransportListing(provider_name='ColdChain Express', vehicle_type='Refrigerated Container', capacity=10.0, price_per_km=65.0, contact_phone='9812345679', service_areas='Delhi NCR, Haryana, Punjab', is_refrigerated=True, rating=4.9),
        ]
        db.session.add_all(transports)

    db.session.commit()
    click.echo('Demo data seeding completed successfully!')
