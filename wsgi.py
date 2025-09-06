#!/usr/bin/env python
"""
WSGI entry point for the Flask application.
This file is used by Gunicorn to start the app.
"""
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app from the app directory
from app.app import app

if __name__ == "__main__":
    app.run()
