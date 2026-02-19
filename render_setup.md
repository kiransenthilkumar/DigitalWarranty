"""
Render.com Deployment Setup Instructions

1. Connect your GitHub repository to Render
2. Create a new Web Service on Render
3. Use the following settings:
"""

# Service Configuration:
# - Build Command: pip install -r requirements.txt
# - Start Command: gunicorn wsgi:app
# - Environment: Python 3.10
# - Plan: Free (or paid for production)

# Environment Variables to set in Render Dashboard:
{
    "FLASK_ENV": "production",
    "FLASK_DEBUG": "0",
    "SECRET_KEY": "your-very-secure-secret-key-here",
    # Optional: PostgreSQL for production
    # "DATABASE_URL": "postgresql://user:password@host/dbname"
}
