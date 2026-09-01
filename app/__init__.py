"""Compatibility package for the legacy root-level Flask application.

The original project keeps the application factory at the repository root,
while routes/models/extensions live under the app package. Re-exporting the
factory here makes imports such as ``from app import create_app`` work on
Vercel and locally without changing the existing project layout.
"""
from importlib import import_module

create_app = import_module("__init__").create_app

__all__ = ["create_app"]
