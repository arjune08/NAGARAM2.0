"""
NAGARAM — Vercel Serverless Entry Point
"""
from app import create_app

app = create_app('production')
