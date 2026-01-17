"""
Simple test endpoint for Vercel debugging
"""
import os
import sys
from flask import Flask

app = Flask(__name__)

@app.route('/')
def test():
    return {
        'status': 'working',
        'python_version': sys.version,
        'python_path': sys.path,
        'environment_variables': {
            'VERCEL': os.environ.get('VERCEL'),
            'FLASK_ENV': os.environ.get('FLASK_ENV'),
            'DATABASE_URL': 'SET' if os.environ.get('DATABASE_URL') else 'NOT SET',
            'SECRET_KEY': 'SET' if os.environ.get('SECRET_KEY') else 'NOT SET'
        },
        'current_directory': os.getcwd(),
        'files_in_directory': os.listdir('.')
    }

@app.route('/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    app.run()