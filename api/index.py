import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set environment for Vercel
os.environ.setdefault('VERCEL', '1')
os.environ.setdefault('FLASK_ENV', 'production')

try:
    from app import create_app
    app = create_app()
except ImportError as e:
    # Fallback error app
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def import_error():
        return f"Import Error: {str(e)}<br>Python Path: {sys.path}", 500
    
    @app.route('/<path:path>')
    def catch_all(path):
        return f"Import Error: {str(e)}", 500

except Exception as e:
    # Fallback error app for other errors
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def general_error():
        return f"Application Error: {str(e)}", 500
    
    @app.route('/<path:path>')
    def catch_all_error(path):
        return f"Application Error: {str(e)}", 500