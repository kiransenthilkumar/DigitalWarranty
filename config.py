import os

class Config:
    # Get secret key from environment, use fallback for development only
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Ensure instance folder exists for local development
    INSTANCE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    os.makedirs(INSTANCE_PATH, exist_ok=True)
    
    # Database configuration
    # On Render: uses PostgreSQL via DATABASE_URL environment variable
    # Local: falls back to SQLite
    if os.environ.get('DATABASE_URL'):
        # PostgreSQL on Render (or other hosted DB)
        # Ensure SSL mode is required and enable pool pre-ping to handle
        # Render's occasional closed connections.
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
        # Add engine options for SSL and liveliness checks
        SQLALCHEMY_ENGINE_OPTIONS = {
            'connect_args': {'sslmode': 'require'},
            'pool_pre_ping': True,
        }
    else:
        # SQLite for local development
        _db_path = os.path.join(INSTANCE_PATH, 'warranty.db')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{_db_path}'.replace('\\', '/')
        SQLALCHEMY_ENGINE_OPTIONS = {}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload folder configuration
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'webp', 'avif'}
    
    @staticmethod
    def ensure_dirs():
        """Create necessary directories if they don't exist"""
        os.makedirs(Config.INSTANCE_PATH, exist_ok=True)
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Ensure directories on config import
Config.ensure_dirs()

