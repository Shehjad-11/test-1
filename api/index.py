import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set environment for Vercel
os.environ.setdefault('VERCEL', '1')
os.environ.setdefault('FLASK_ENV', 'production')

from flask import Flask

# Create a simple test app first
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key')

@app.route('/')
def home():
    return '''
    <h1>🎉 Flask App is Working on Vercel!</h1>
    <p>Your deployment is successful!</p>
    <ul>
        <li><a href="/test">Test Database Connection</a></li>
        <li><a href="/debug">Debug Info</a></li>
    </ul>
    '''

@app.route('/test')
def test_db():
    try:
        # Try to import and test the full app
        from app import create_app
        test_app = create_app()
        with test_app.app_context():
            from app import db
            # Test database connection
            db.engine.execute('SELECT 1')
            return '<h2>✅ Database Connection Working!</h2><p><a href="/">Back to Home</a></p>'
    except Exception as e:
        return f'<h2>❌ Database Error:</h2><p>{str(e)}</p><p><a href="/">Back to Home</a></p>'

@app.route('/debug')
def debug():
    return {
        'status': 'working',
        'python_version': sys.version,
        'environment_variables': {
            'VERCEL': os.environ.get('VERCEL'),
            'FLASK_ENV': os.environ.get('FLASK_ENV'),
            'DATABASE_URL': 'SET' if os.environ.get('DATABASE_URL') else 'NOT SET',
            'SECRET_KEY': 'SET' if os.environ.get('SECRET_KEY') else 'NOT SET'
        },
        'current_directory': os.getcwd(),
        'python_path': sys.path[:3]  # First 3 entries
    }

@app.route('/full-app')
def full_app():
    try:
        # Try to load the full app
        from app import create_app
        full_app = create_app()
        return '<h2>✅ Full App Loaded Successfully!</h2><p>Ready to enable full functionality.</p>'
    except Exception as e:
        return f'<h2>❌ Full App Error:</h2><p>{str(e)}</p>'

if __name__ == '__main__':
    app.run(debug=False)