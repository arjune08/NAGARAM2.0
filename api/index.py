"""NAGARAM — Vercel Serverless Entry Point."""

# Keep the Vercel entry point inside the real application package. This avoids
# importing the legacy root-level __init__.py and prevents circular imports.
from app import create_app

app = create_app("production")
