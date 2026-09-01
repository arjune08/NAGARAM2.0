"""
NAGARAM — Crop Recommendation Service
Rule-based crop recommendation engine.
Designed so the rule engine can be replaced with an ML model later.
"""


# Crop database: maps (soil_type, season, water) → suitable crops
CROP_DATABASE = {
    ('Alluvial', 'Kharif', 'High'): [
        {'name': 'Rice (Paddy)', 'suitability': 95, 'yield_range': '40-60 Q/ha',
         'notes': 'Highly suitable for irrigated alluvial soils in Kharif season.'},
        {'name': 'Sugarcane', 'suitability': 85, 'yield_range': '600-800 Q/ha',
         'notes': 'Excellent in alluvial soil with good water supply.'},
        {'name': 'Jute', 'suitability': 80, 'yield_range': '20-30 Q/ha',
         'notes': 'Requires warm humid climate and good water.'},
    ],
    ('Alluvial', 'Rabi', 'High'): [
        {'name': 'Wheat', 'suitability': 90, 'yield_range': '35-50 Q/ha',
         'notes': 'Alluvial soil is ideal for wheat in Rabi.'},
        {'name': 'Mustard', 'suitability': 80, 'yield_range': '10-15 Q/ha',
         'notes': 'Good in well-drained alluvial soils.'},
        {'name': 'Potato', 'suitability': 85, 'yield_range': '200-300 Q/ha',
         'notes': 'Performs well with irrigation in alluvial soil.'},
    ],
    ('Black', 'Kharif', 'Medium'): [
        {'name': 'Cotton', 'suitability': 92, 'yield_range': '15-25 Q/ha',
         'notes': 'Black soil is ideal for cotton cultivation.'},
        {'name': 'Soybean', 'suitability': 88, 'yield_range': '15-25 Q/ha',
         'notes': 'Excellent in black soil with moderate water.'},
        {'name': 'Sorghum (Jowar)', 'suitability': 82, 'yield_range': '20-35 Q/ha',
         'notes': 'Drought-tolerant, good in black soils.'},
    ],
    ('Black', 'Rabi', 'Medium'): [
        {'name': 'Wheat', 'suitability': 85, 'yield_range': '30-45 Q/ha',
         'notes': 'Good in black soil with some irrigation.'},
        {'name': 'Chickpea (Gram)', 'suitability': 90, 'yield_range': '10-18 Q/ha',
         'notes': 'Thrives in black soil during Rabi with moderate moisture.'},
        {'name': 'Linseed', 'suitability': 75, 'yield_range': '8-12 Q/ha',
         'notes': 'Suitable for heavy black soils.'},
    ],
    ('Red', 'Kharif', 'Low'): [
        {'name': 'Millet (Ragi)', 'suitability': 90, 'yield_range': '15-25 Q/ha',
         'notes': 'Excellent in red soils with low water. Highly nutritious.'},
        {'name': 'Groundnut', 'suitability': 85, 'yield_range': '15-20 Q/ha',
         'notes': 'Well-suited for red sandy soils.'},
        {'name': 'Pigeon Pea (Tur)', 'suitability': 80, 'yield_range': '8-15 Q/ha',
         'notes': 'Drought tolerant, fixes nitrogen in soil.'},
    ],
    ('Red', 'Rabi', 'Low'): [
        {'name': 'Safflower', 'suitability': 82, 'yield_range': '8-12 Q/ha',
         'notes': 'Good in red soils, drought tolerant.'},
        {'name': 'Horse Gram', 'suitability': 85, 'yield_range': '5-8 Q/ha',
         'notes': 'Thrives in poor, dry red soils.'},
    ],
    ('Laterite', 'Kharif', 'Medium'): [
        {'name': 'Cashew', 'suitability': 88, 'yield_range': '8-12 Q/ha',
         'notes': 'Laterite soils are ideal for cashew plantations.'},
        {'name': 'Rubber', 'suitability': 85, 'yield_range': '1500-2000 kg/ha',
         'notes': 'Thrives in laterite soil with adequate rainfall.'},
        {'name': 'Tapioca', 'suitability': 82, 'yield_range': '250-350 Q/ha',
         'notes': 'Well-suited for laterite soils.'},
    ],
    ('Sandy', 'Kharif', 'Low'): [
        {'name': 'Pearl Millet (Bajra)', 'suitability': 90, 'yield_range': '12-20 Q/ha',
         'notes': 'Excellent drought tolerance. Ideal for sandy soils.'},
        {'name': 'Cluster Bean (Guar)', 'suitability': 85, 'yield_range': '8-12 Q/ha',
         'notes': 'Thrives in sandy soils with minimal water.'},
        {'name': 'Sesame', 'suitability': 78, 'yield_range': '4-6 Q/ha',
         'notes': 'Suitable for light sandy soils.'},
    ],
    ('Loamy', 'Kharif', 'High'): [
        {'name': 'Maize', 'suitability': 92, 'yield_range': '50-70 Q/ha',
         'notes': 'Loamy soils with good drainage are ideal for maize.'},
        {'name': 'Rice (Paddy)', 'suitability': 88, 'yield_range': '40-55 Q/ha',
         'notes': 'Good in loamy soils with water availability.'},
        {'name': 'Vegetables', 'suitability': 90, 'yield_range': 'Varies',
         'notes': 'Loamy soil is excellent for most vegetable crops.'},
    ],
    ('Loamy', 'Rabi', 'Medium'): [
        {'name': 'Wheat', 'suitability': 92, 'yield_range': '40-55 Q/ha',
         'notes': 'Loamy soils are ideal for wheat.'},
        {'name': 'Peas', 'suitability': 85, 'yield_range': '60-80 Q/ha',
         'notes': 'Well-suited for cool-season loamy soil cultivation.'},
        {'name': 'Barley', 'suitability': 80, 'yield_range': '25-35 Q/ha',
         'notes': 'Performs well in loamy soils during Rabi.'},
    ],
    ('Clay', 'Kharif', 'High'): [
        {'name': 'Rice (Paddy)', 'suitability': 95, 'yield_range': '45-65 Q/ha',
         'notes': 'Clay soils retain water, making them ideal for paddy.'},
        {'name': 'Sugarcane', 'suitability': 80, 'yield_range': '500-700 Q/ha',
         'notes': 'Good with heavy irrigation in clay soils.'},
    ],
    ('Clay Loam', 'Kharif', 'Medium'): [
        {'name': 'Cotton', 'suitability': 88, 'yield_range': '15-25 Q/ha',
         'notes': 'Clay loam retains moisture well for cotton.'},
        {'name': 'Soybean', 'suitability': 85, 'yield_range': '15-25 Q/ha',
         'notes': 'Good in clay loam with moderate irrigation.'},
    ],
    ('Sandy Loam', 'Kharif', 'Medium'): [
        {'name': 'Groundnut', 'suitability': 90, 'yield_range': '15-22 Q/ha',
         'notes': 'Sandy loam is excellent for groundnut cultivation.'},
        {'name': 'Sunflower', 'suitability': 82, 'yield_range': '12-18 Q/ha',
         'notes': 'Well-drained sandy loam is suitable.'},
        {'name': 'Maize', 'suitability': 85, 'yield_range': '45-65 Q/ha',
         'notes': 'Good in sandy loam with adequate moisture.'},
    ],
}

# Fallback general recommendations
GENERAL_RECOMMENDATIONS = [
    {'name': 'Millets', 'suitability': 75, 'yield_range': '10-20 Q/ha',
     'notes': 'Millets are versatile, drought-tolerant, and suitable for most soil types.'},
    {'name': 'Pulses (Mixed)', 'suitability': 70, 'yield_range': '8-15 Q/ha',
     'notes': 'Pulses fix nitrogen and are generally adaptable. Consult local expert for specific variety.'},
    {'name': 'Vegetables', 'suitability': 65, 'yield_range': 'Varies',
     'notes': 'Choose vegetables suited to your local climate and market demand.'},
]


def get_crop_recommendations(soil_type, season, water_availability,
                              ph=None, previous_crop=None, location=None):
    """
    Get crop recommendations based on input parameters.
    Uses a rule-based lookup with fallback.
    This function can be replaced with an ML model later.

    Returns: dict with 'recommendations' list and 'source' indicator.
    """
    key = (soil_type, season, water_availability)
    recommendations = CROP_DATABASE.get(key)

    if not recommendations:
        # Try partial matches
        for db_key, crops in CROP_DATABASE.items():
            if db_key[0] == soil_type and db_key[1] == season:
                recommendations = crops
                break

    if not recommendations:
        for db_key, crops in CROP_DATABASE.items():
            if db_key[0] == soil_type:
                recommendations = crops
                break

    if not recommendations:
        recommendations = GENERAL_RECOMMENDATIONS

    # Adjust suitability based on pH if provided
    if ph is not None:
        for rec in recommendations:
            if ph < 5.5 or ph > 8.5:
                rec['suitability'] = max(rec['suitability'] - 15, 30)
                rec['notes'] += ' ⚠️ Soil pH may affect yield. Consider soil treatment.'

    # Add rotation note if previous crop is provided
    rotation_note = ''
    if previous_crop:
        rotation_note = f'Previous crop was {previous_crop}. Consider crop rotation for soil health.'

    return {
        'source': 'Rule-Based Engine (Demo)',
        'parameters': {
            'soil_type': soil_type,
            'season': season,
            'water': water_availability,
            'ph': ph,
            'previous_crop': previous_crop,
        },
        'recommendations': recommendations,
        'rotation_note': rotation_note,
    }
