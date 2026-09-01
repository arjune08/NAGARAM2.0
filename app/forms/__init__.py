"""Expose root-level forms under the legacy app.forms namespace."""
import os

__path__ = [os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "forms"))]
