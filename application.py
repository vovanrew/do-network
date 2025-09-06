#!/usr/bin/env python
"""
Root app.py file for Render deployment.
This file exists to satisfy Render's auto-detection.
"""
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app from the app directory
from app.app import app as application

# Export it as 'app' so gunicorn can find it
app = application
