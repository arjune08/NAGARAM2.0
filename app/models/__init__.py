"""Expose root-level models under the legacy app.models namespace."""
import os

__path__ = [os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models"))]
