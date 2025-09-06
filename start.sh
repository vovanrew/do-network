#!/bin/bash
# Start script for Render deployment
echo "Starting application with gunicorn..."
gunicorn wsgi:app --bind 0.0.0.0:$PORT
