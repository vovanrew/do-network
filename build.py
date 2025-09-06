#!/usr/bin/env python
"""
Build script for initializing the database on Render
"""
import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import app
from models import db

def init_database():
    """Initialize the database with tables"""
    with app.app_context():
        # Create the instance directory if it doesn't exist
        instance_path = os.path.join(os.path.dirname(__file__), 'app', 'instance')
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)
        
        # Create all tables
        db.create_all()
        print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()
