"""NAGARAM — Vercel Serverless Entry Point."""

# Vercel executes this module from the repository root. Import the Flask
# application factory explicitly from the root package so it works in the
# Vercel Python runtime as well as local development.
from __init__ import create_app

app = create_app("production")
