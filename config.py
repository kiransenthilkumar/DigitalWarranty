import os

class Config:
    # Get secret key from environment, use fallback for development only
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Determine instance path - use Render persistent disk if available
    if os.environ.get('RENDER'):
        # On Render, use the persistent disk mount point
        INSTANCE_PATH = '/opt/render/project/src/instance'
    else:
        # Local development
        INSTANCE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    
    os.makedirs(INSTANCE_PATH, exist_ok=True)
    
    # Database configuration - use correct SQLite path
    _db_path = os.path.join(INSTANCE_PATH, 'warranty.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{_db_path}'.replace('\\', '/')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload folder configuration
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'static/uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'webp', 'avif'}
    
    @staticmethod
    def ensure_dirs():
        """Create necessary directories if they don't exist"""
        os.makedirs(Config.INSTANCE_PATH, exist_ok=True)
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Ensure directories on config import
Config.ensure_dirs()

