"""Expose root-level routes under the legacy app.routes namespace."""
import os

__path__ = [os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "routes"))]
