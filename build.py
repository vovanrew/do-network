#!/usr/bin/env python
"""
Build script for initializing the database on Render
"""
import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from app.app import app
from app.models import db

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
