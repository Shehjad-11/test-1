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
    # Try to import and create the full app
    from app import create_app
    app = create_app()
    
    # Add a test route to verify it's working
    @app.route('/vercel-test')
    def vercel_test():
        return '''
        <h1>🎉 Full Flask App Working on Vercel!</h1>
        <p>✅ All imports successful</p>
        <p>✅ Database configured</p>
        <p>✅ All routes loaded</p>
        <ul>
            <li><a href="/">Homepage</a></li>
            <li><a href="/auth/register">Register</a></li>
            <li><a href="/auth/login">Login</a></li>
            <li><a href="/messages">Messages</a></li>
            <li><a href="/notifications">Notifications</a></li>
        </ul>
        '''

except Exception as e:
    # Create fallback app with error info
    from flask import Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key')
    
    @app.route('/')
    def error_info():
        return f'''
        <h1>❌ App Loading Error</h1>
        <p><strong>Error:</strong> {str(e)}</p>
        <p><strong>Type:</strong> {type(e).__name__}</p>
        <p><a href="/debug">Debug Info</a></p>
        '''
    
    @app.route('/debug')
    def debug():
        import traceback
        return f'''
        <h2>Debug Information</h2>
        <p><strong>Error:</strong> {str(e)}</p>
        <p><strong>Traceback:</strong></p>
        <pre>{traceback.format_exc()}</pre>
        <p><strong>Python Path:</strong> {sys.path[:5]}</p>
        <p><strong>Environment:</strong></p>
        <ul>
            <li>VERCEL: {os.environ.get('VERCEL')}</li>
            <li>DATABASE_URL: {'SET' if os.environ.get('DATABASE_URL') else 'NOT SET'}</li>
            <li>SECRET_KEY: {'SET' if os.environ.get('SECRET_KEY') else 'NOT SET'}</li>
        </ul>
        '''

if __name__ == '__main__':
    app.run(debug=False)