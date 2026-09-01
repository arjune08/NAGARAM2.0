"""
NAGARAM — Market Service
Market intelligence data service with demo data.
Designed for future integration with Agmarknet or eNAM APIs.
"""
from datetime import date, timedelta


def get_market_prices(commodity=None, market=None, district=None):
    """
    Get current market prices for agricultural commodities.
    Returns demo data.
    """
    demo_prices = [
        {'commodity': 'Rice (Paddy)', 'variety': 'Common', 'market': 'Koyambedu',
         'district': 'Chennai', 'min_price': 1800, 'max_price': 2200,
         'modal_price': 2040, 'unit': 'Quintal', 'date': str(date.today())},
        {'commodity': 'Wheat', 'variety': 'Lokwan', 'market': 'Indore Mandi',
         'district': 'Indore', 'min_price': 2100, 'max_price': 2400,
         'modal_price': 2275, 'unit': 'Quintal', 'date': str(date.today())},
        {'commodity': 'Cotton', 'variety': 'Medium Staple', 'market': 'Rajkot',
         'district': 'Rajkot', 'min_price': 5600, 'max_price': 6200,
         'modal_price': 5950, 'unit': 'Quintal', 'date': str(date.today())},
        {'commodity': 'Tomato', 'variety': 'Local', 'market': 'Koyambedu',
         'district': 'Chennai', 'min_price': 1200, 'max_price': 2000,
         'modal_price': 1600, 'unit': 'Quintal', 'date': str(date.today())},
        {'commodity': 'Onion', 'variety': 'Red', 'market': 'Lasalgaon',
         'district': 'Nashik', 'min_price': 800, 'max_price': 1400,
         'modal_price': 1100, 'unit': 'Quintal', 'date': str(date.today())},
        {'commodity': 'Potato', 'variety': 'Jyoti', 'market': 'Agra Mandi',
         'district': 'Agra', 'min_price': 600, 'max_price': 900,
         'modal_price': 750, 'unit': 'Quintal', 'date': str(date.today())},
        {'commodity': 'Soybean', 'variety': 'Yellow', 'market': 'Indore Mandi',
         'district': 'Indore', 'min_price': 4200, 'max_price': 4800,
         'modal_price': 4500, 'unit': 'Quintal', 'date': str(date.today())},
        {'commodity': 'Sugarcane', 'variety': 'Common', 'market': 'Kolhapur',
         'district': 'Kolhapur', 'min_price': 280, 'max_price': 320,
         'modal_price': 305, 'unit': 'Quintal', 'date': str(date.today())},
    ]

    # Filter if criteria provided
    results = demo_prices
    if commodity:
        results = [p for p in results if commodity.lower() in p['commodity'].lower()]
    if district:
        results = [p for p in results if district.lower() in p['district'].lower()]

    return {'source': 'Demo Data', 'prices': results}


def get_price_trends(commodity='Rice (Paddy)', days=30):
    """
    Get price trend data for a commodity.
    Returns demo data suitable for charting.
    """
    import random
    random.seed(42)
    base_price = 2000
    trends = []
    for i in range(days):
        d = date.today() - timedelta(days=days - i - 1)
        variation = random.randint(-100, 100)
        trends.append({
            'date': str(d),
            'price': base_price + variation,
        })
        base_price = base_price + random.randint(-20, 25)

    return {
        'source': 'Demo Data',
        'commodity': commodity,
        'trends': trends,
    }


def get_nearby_markets(lat=None, lon=None, district=None):
    """
    Get nearby market information.
    Returns demo data.
    """
    return {
        'source': 'Demo Data',
        'markets': [
            {'name': 'Koyambedu Wholesale Market', 'district': 'Chennai',
             'distance_km': 12, 'type': 'Wholesale', 'operating_days': 'Mon-Sat'},
            {'name': 'Thirumangalam APMC', 'district': 'Chennai',
             'distance_km': 8, 'type': 'APMC', 'operating_days': 'Mon-Sat'},
            {'name': 'Pallavaram Market', 'district': 'Chennai',
             'distance_km': 15, 'type': 'Retail', 'operating_days': 'Daily'},
        ],
    }
