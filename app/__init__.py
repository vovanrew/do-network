"""
Make the Flask app available at the package level.
This allows 'from app import app' to work.
"""
from .app import app

__all__ = ['app']

