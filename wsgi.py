"""
WSGI entry point for production deployment
This file is used by production servers like Gunicorn
"""

from app import app, init_db

# Initialize database when the WSGI app starts
if __name__ != '__main__':
    init_db()

if __name__ == '__main__':
    app.run()
