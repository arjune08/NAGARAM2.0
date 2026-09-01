"""
NAGARAM — Government Scheme Service
Scheme eligibility matching service with demo scheme data.
"""


DEMO_SCHEMES = [
    {
        'name': 'PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)',
        'scheme_code': 'PMKISAN',
        'department': 'Ministry of Agriculture & Farmers Welfare',
        'scheme_type': 'subsidy',
        'description': 'Income support of ₹6,000 per year to all landholding farmer families, paid in three equal instalments of ₹2,000 each.',
        'benefits': '₹6,000 per year directly to bank account in 3 instalments.',
        'eligibility': 'All landholding farmer families with cultivable land. Small and marginal farmers are prioritized.',
        'required_documents': 'Aadhar Card, Land ownership documents, Bank account details, Mobile number',
        'application_process': 'Apply online through PM-KISAN portal or visit nearest Common Service Centre (CSC).',
        'application_url': 'https://pmkisan.gov.in',
        'max_benefit_amount': 6000,
        'target_group': 'all_farmers',
        'min_land_holding': 0,
        'max_land_holding': None,
        'applicable_states': 'All India',
    },
    {
        'name': 'Pradhan Mantri Fasal Bima Yojana (PMFBY)',
        'scheme_code': 'PMFBY',
        'department': 'Ministry of Agriculture & Farmers Welfare',
        'scheme_type': 'insurance',
        'description': 'Crop insurance scheme providing financial support to farmers suffering crop loss/damage due to unforeseen events.',
        'benefits': 'Insurance coverage for crop loss due to natural calamities, pests, and diseases. Premium: 2% for Kharif, 1.5% for Rabi crops.',
        'eligibility': 'All farmers growing notified crops in notified areas. Both loanee and non-loanee farmers.',
        'required_documents': 'Aadhar Card, Land records, Bank passbook, Sowing certificate, Previous season crop details',
        'application_process': 'Apply through bank, CSC, or PMFBY portal before sowing season deadline.',
        'application_url': 'https://pmfby.gov.in',
        'max_benefit_amount': None,
        'target_group': 'all_farmers',
        'min_land_holding': 0,
        'max_land_holding': None,
        'applicable_states': 'All India',
    },
    {
        'name': 'Kisan Credit Card (KCC)',
        'scheme_code': 'KCC',
        'department': 'Ministry of Finance / NABARD',
        'scheme_type': 'loan',
        'description': 'Provides affordable credit to farmers for agricultural and allied activities at subsidized interest rates.',
        'benefits': 'Short-term credit at 4% interest (with subvention). Credit limit based on land holding and crop.',
        'eligibility': 'All farmers — individual, joint, tenant, sharecroppers, SHGs. Must have cultivable land or allied activity.',
        'required_documents': 'Aadhar Card, Land records, Identity proof, Passport photos, Recent passport-size photos',
        'application_process': 'Apply at nearest bank branch (commercial, cooperative, or RRB).',
        'application_url': None,
        'max_benefit_amount': 300000,
        'target_group': 'all_farmers',
        'min_land_holding': 0,
        'max_land_holding': None,
        'applicable_states': 'All India',
    },
    {
        'name': 'Soil Health Card Scheme',
        'scheme_code': 'SHC',
        'department': 'Ministry of Agriculture & Farmers Welfare',
        'scheme_type': 'grant',
        'description': 'Provides soil health cards to farmers with crop-wise nutrient recommendations to improve soil fertility and farm productivity.',
        'benefits': 'Free soil testing, personalized soil health card with nutrient status and fertilizer recommendations.',
        'eligibility': 'All farmers across India.',
        'required_documents': 'Aadhar Card, Land details',
        'application_process': 'Contact nearest Krishi Vigyan Kendra (KVK) or agriculture department office.',
        'application_url': 'https://soilhealth.dac.gov.in',
        'max_benefit_amount': None,
        'target_group': 'all_farmers',
        'min_land_holding': 0,
        'max_land_holding': None,
        'applicable_states': 'All India',
    },
    {
        'name': 'PM Micro Irrigation Fund (PMKSY-PDMC)',
        'scheme_code': 'PMKSY',
        'department': 'Ministry of Agriculture & Farmers Welfare',
        'scheme_type': 'subsidy',
        'description': 'Promotes micro irrigation (drip/sprinkler) with subsidy support for water-use efficiency.',
        'benefits': 'Subsidy of 55% for small/marginal farmers and 45% for others on micro irrigation systems.',
        'eligibility': 'All farmers. Higher subsidy for small and marginal farmers (land < 5 acres).',
        'required_documents': 'Aadhar Card, Land documents, Bank details, Caste certificate (if SC/ST)',
        'application_process': 'Apply through state agriculture department or district agriculture office.',
        'application_url': 'https://pmksy.gov.in',
        'max_benefit_amount': None,
        'target_group': 'small_farmer',
        'min_land_holding': 0,
        'max_land_holding': 5,
        'applicable_states': 'All India',
    },
    {
        'name': 'National Mission on Sustainable Agriculture (NMSA)',
        'scheme_code': 'NMSA',
        'department': 'Ministry of Agriculture & Farmers Welfare',
        'scheme_type': 'subsidy',
        'description': 'Promotes sustainable agriculture through soil health management, water-use efficiency, and climate-resilient practices.',
        'benefits': 'Financial assistance for organic farming inputs, soil amendments, and training.',
        'eligibility': 'Farmer groups, FPOs, and individual farmers practicing or transitioning to sustainable farming.',
        'required_documents': 'Aadhar Card, Land records, Group registration (if applicable)',
        'application_process': 'Apply through district agriculture office or state agriculture department portal.',
        'application_url': None,
        'max_benefit_amount': 50000,
        'target_group': 'all_farmers',
        'min_land_holding': 0,
        'max_land_holding': None,
        'applicable_states': 'All India',
    },
]


def get_all_schemes():
    """Get all government schemes."""
    return {'source': 'Demo Data', 'schemes': DEMO_SCHEMES}


def check_eligibility(land_holding=None, farmer_type=None, state=None):
    """
    Check scheme eligibility based on farmer parameters.
    Returns eligible schemes with match reasons.

    This is a simple rule-based matcher — not a legal determination.
    """
    eligible = []

    for scheme in DEMO_SCHEMES:
        match = True
        reasons = []

        # Check land holding
        if land_holding is not None:
            if scheme['min_land_holding'] is not None and land_holding < scheme['min_land_holding']:
                match = False
            if scheme['max_land_holding'] is not None and land_holding > scheme['max_land_holding']:
                match = False
            else:
                reasons.append('Land holding within eligible range')

        # Check target group
        if farmer_type and scheme['target_group'] not in ['all_farmers', farmer_type]:
            match = False
        else:
            reasons.append('Farmer category eligible')

        # Check state
        if state and scheme['applicable_states'] != 'All India':
            if state not in scheme['applicable_states']:
                match = False
        else:
            reasons.append('Applicable in your state')

        if match:
            eligible.append({
                **scheme,
                'match_reasons': reasons,
            })

    return {
        'source': 'Demo Data (Not a legal determination)',
        'disclaimer': 'Eligibility shown is indicative only. Please verify with the relevant government office.',
        'eligible_schemes': eligible,
    }
