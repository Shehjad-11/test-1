import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-vercel-deployment'
    
    # Database configuration for Vercel
    # Use PostgreSQL for production, SQLite for development
    if os.environ.get('VERCEL'):
        # Production on Vercel - use PostgreSQL
        database_url = os.environ.get('DATABASE_URL') or os.environ.get('POSTGRES_URL')
        if database_url:
            if database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql://', 1)
            SQLALCHEMY_DATABASE_URI = database_url
        else:
            # Fallback to SQLite if no PostgreSQL URL provided
            SQLALCHEMY_DATABASE_URI = 'sqlite:///temp_collaboration_platform.db'
    else:
        # Development - use SQLite
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///collaboration_platform.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # File upload configuration
    UPLOAD_FOLDER = 'app/static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Vercel-specific configurations
    if os.environ.get('VERCEL'):
        # Disable file uploads on Vercel (serverless doesn't support persistent file storage)
        MAX_CONTENT_LENGTH = 0