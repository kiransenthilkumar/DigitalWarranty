# Digital Warranty Application - Deployment Guide

## Database Persistence Issues - FIXED ✅

### Problem (Previously)
The database was auto-resetting and reverting to default seeding on each deployment because:
1. Database initialization code was inside `if __name__ == '__main__':` 
2. This code doesn't execute when using a WSGI server (Gunicorn, uWSGI, etc.)
3. The database wasn't being created/persisted on production

### Solution Implemented
1. **Moved database initialization** outside the main block to run on each deployment
2. **Created WSGI entry point** (`wsgi.py`) for production servers
3. **Updated config.py** to use a persistent `instance/` folder
4. **Added automatic directory creation** to ensure folders exist

## Deployment Steps

### For Development
```bash
python app.py
```

### For Production with Gunicorn
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app
```

### For Other WSGI Servers
Use `wsgi.py` as your application module:
- **uWSGI**: `uwsgi --http :5000 --wsgi-file wsgi.py --callable app`
- **Waitress**: `waitress-serve --port=5000 wsgi:app`

## Environment Variables for Production

```bash
# Security
SECRET_KEY=your-very-secure-random-key-here

# Database (optional, defaults to SQLite)
DATABASE_URL=postgresql://user:password@localhost/warranty_db

# Upload folder
UPLOAD_FOLDER=/var/www/warranty/uploads

# Flask
FLASK_ENV=production
FLASK_DEBUG=0
```

## Database Persistence Checklist

- ✅ Database is now stored in `instance/warranty.db`
- ✅ Database initialization runs on every deployment
- ✅ Seeding only happens if no users exist
- ✅ Data persists between restarts
- ✅ Works with both `python app.py` and WSGI servers

## File Structure
```
DigitalWarranty/
├── app.py                 # Main Flask app (with init code)
├── wsgi.py               # Production WSGI entry point
├── config.py             # Configuration (persistent paths)
├── instance/             # Persistent data (git-ignored)
│   └── warranty.db       # SQLite database
├── static/
│   ├── uploads/          # User uploads (git-ignored)
│   └── ...
└── templates/
```

## Troubleshooting

### Database still resetting?
1. Check that `instance/` folder has write permissions
2. Verify `SQLALCHEMY_DATABASE_URI` points to a persistent location
3. Ensure `static/uploads/` folder exists and is writable

### Seeding running every time?
This is intentional! The code checks if users exist first:
```python
if User.query.first() is None:
    seed_db()
```
So seed_db() only runs when the database is empty.

### Files in uploads folder disappearing?
1. Add `static/uploads/.gitkeep` to version control
2. Ignore `static/uploads/*` in `.gitignore`
3. Mount uploads to a persistent volume on deployment platforms
