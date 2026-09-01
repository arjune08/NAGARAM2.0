"""Compatibility wrapper for the project's weather service.

The implementation lives in the legacy top-level services package. This
module keeps the app.services import path working on Vercel.
"""
from services.weather_service import *
