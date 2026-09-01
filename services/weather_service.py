"""
NAGARAM — Weather Service
Weather data service with demo data fallback.
Designed for future integration with OpenWeatherMap or IMD API.
"""


def get_current_weather(lat=None, lon=None, location=None):
    """
    Get current weather data.
    Returns demo data — replace with real API call when credentials available.
    """
    # TODO: Replace with actual API call
    # Example: requests.get(f'https://api.openweathermap.org/data/2.5/weather?...')
    return {
        'source': 'Demo Data',
        'location': location or 'Sample Location',
        'temperature': 32,
        'feels_like': 35,
        'humidity': 68,
        'wind_speed': 12,
        'wind_direction': 'SW',
        'pressure': 1008,
        'condition': 'Partly Cloudy',
        'icon': 'cloud-sun',
        'rainfall_today': 0,
        'visibility': 8,
        'uv_index': 7,
    }


def get_weather_forecast(lat=None, lon=None, location=None, days=5):
    """
    Get weather forecast.
    Returns demo data.
    """
    forecasts = [
        {'day': 'Today', 'high': 34, 'low': 26, 'condition': 'Partly Cloudy',
         'humidity': 65, 'rainfall': 0, 'icon': 'cloud-sun'},
        {'day': 'Tomorrow', 'high': 33, 'low': 25, 'condition': 'Sunny',
         'humidity': 55, 'rainfall': 0, 'icon': 'sun'},
        {'day': 'Day 3', 'high': 31, 'low': 24, 'condition': 'Light Rain',
         'humidity': 78, 'rainfall': 12, 'icon': 'cloud-rain'},
        {'day': 'Day 4', 'high': 30, 'low': 23, 'condition': 'Thunderstorm',
         'humidity': 85, 'rainfall': 35, 'icon': 'cloud-lightning'},
        {'day': 'Day 5', 'high': 32, 'low': 25, 'condition': 'Cloudy',
         'humidity': 70, 'rainfall': 5, 'icon': 'cloud'},
    ]
    return {
        'source': 'Demo Data',
        'location': location or 'Sample Location',
        'forecasts': forecasts[:days],
    }


def get_farming_alerts(location=None):
    """
    Get weather-based farming alerts.
    Returns demo alerts.
    """
    return {
        'source': 'Demo Data',
        'alerts': [
            {
                'type': 'warning',
                'title': 'Heavy Rain Expected',
                'message': 'Heavy rainfall expected in 2-3 days. Consider postponing pesticide spraying and secure harvested produce.',
                'severity': 'moderate',
            },
            {
                'type': 'info',
                'title': 'Good Conditions for Sowing',
                'message': 'Soil moisture and temperature are favorable for Rabi crop sowing this week.',
                'severity': 'low',
            },
        ],
    }


def get_water_advisory(lat=None, lon=None, location=None, crop=None):
    """
    Get irrigation and water advisory data.
    Returns demo data.
    """
    return {
        'source': 'Demo Data',
        'location': location or 'Sample Location',
        'recent_rainfall_mm': 45,
        'soil_moisture_pct': 42,
        'reservoir_level_pct': 68,
        'irrigation_recommended': True,
        'recommended_method': 'Drip Irrigation',
        'water_requirement_mm': 25,
        'next_irrigation': 'In 2 days',
        'crop_water_needs': [
            {'crop': 'Rice (Paddy)', 'daily_mm': 6, 'status': 'Adequate'},
            {'crop': 'Wheat', 'daily_mm': 4, 'status': 'Needs Irrigation'},
            {'crop': 'Cotton', 'daily_mm': 5, 'status': 'Adequate'},
            {'crop': 'Sugarcane', 'daily_mm': 8, 'status': 'Monitor'},
        ],
        'schedule': [
            {'day': 'Monday', 'time': '6:00 AM', 'duration': '30 min', 'method': 'Drip'},
            {'day': 'Wednesday', 'time': '6:00 AM', 'duration': '30 min', 'method': 'Drip'},
            {'day': 'Friday', 'time': '6:00 AM', 'duration': '45 min', 'method': 'Drip'},
        ],
    }
