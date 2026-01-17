from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from datetime import datetime
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Auto-create database tables for production deployment
    if os.environ.get('VERCEL'):
        with app.app_context():
            try:
                # Import models before creating tables
                from app import models
                db.create_all()
                print("Database tables created successfully!")
            except Exception as e:
                print(f"Database creation error: {e}")
                # Continue anyway - app might still work
    
    # Add template filters
    @app.template_filter('days_until')
    def days_until_filter(date):
        if date:
            try:
                delta = date.date() - datetime.utcnow().date()
                return delta.days
            except:
                return 0
        return 0
    
    # Register blueprints
    try:
        from app.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
        
        from app.routes import bp as main_bp
        app.register_blueprint(main_bp)
    except Exception as e:
        print(f"Blueprint registration error: {e}")
        # Create a simple error route
        @app.route('/')
        def error_route():
            return f"Blueprint Error: {str(e)}", 500
    
    return app

# Import models at the end to avoid circular imports
try:
    from app import models
except ImportError as e:
    print(f"Models import error: {e}")