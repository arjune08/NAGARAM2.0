"""Compatibility wrapper for the root-level Flask extensions."""
from extensions import db, login_manager, csrf

__all__ = ["db", "login_manager", "csrf"]
