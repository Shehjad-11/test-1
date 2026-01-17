#!/usr/bin/env python3
"""
Vercel serverless function entry point for Flask app
"""

import os
import sys

# Add the parent directory to the Python path so we can import our app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

# Create the Flask app
app = create_app()

# Vercel expects the app to be available as 'app'
# This is the WSGI application that Vercel will use
if __name__ == "__main__":
    app.run()