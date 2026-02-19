# Deploy Digital Warranty on Render.com

## Quick Start (5 Minutes)

### Step 1: Go to Render

1. Open https://render.com
2. Click "Sign up" → "Continue with GitHub"
3. Authorize Render to access your GitHub account

### Step 2: Create Web Service

1. Click "Create +" → "Web Service"
2. Search for and select "DigitalWarranty" repository
3. Click "Connect"

### Step 3: Configure Service

Fill in the form:

| Field | Value |
|-------|-------|
| **Name** | `digital-warranty` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn wsgi:app` |
| **Instance Type** | Free (or Starter Pro for production) |
| **Region** | Pick closest to you |

### Step 4: Add Environment Variables

Before clicking "Create Web Service":

1. Click "Advanced" (if available)
2. Add environment variables:

```
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-random-32-character-secret-key-here
```

To generate SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(16))"
```

### Step 5: Deploy

1. Click "Create Web Service"
2. Watch the deployment logs
3. When complete, visit your app URL (e.g., `digital-warranty.onrender.com`)

## Your App is Live! 🎉

- **Login**: Use the demo users from database seeding
- **Access Database**: SQLite stored on Render's ephemeral filesystem
- **Uploads**: Files persist in `static/uploads/`

## Demo Credentials

```
Email: admin@gmail.com
Password: admin123

OR

Email: sachin@gmail.com
Password: password

OR

Email: mouli@gmail.com
Password: password
```

## Production Recommendations

### Use PostgreSQL Database

For a production-grade database:

1. On Render dashboard, create PostgreSQL database
2. Copy the DATABASE_URL connection string
3. Add to Web Service environment variables as `DATABASE_URL`
4. Redeploy - app automatically uses PostgreSQL!

**PostgreSQL Benefits:**
- No data loss on app restart
- Better performance
- More reliable than SQLite

### Enable Auto-Deploy

- Enable "Auto-Deploy on Push" to auto-update when pushing to GitHub
- Always keep code on main branch in sync with production

### Monitor Your App

- **Logs**: View in Events tab
- **Metrics**: Track CPU/memory usage
- **Restart**: Manual restart if needed

## Troubleshooting

### "502 Bad Gateway" Error
- Check logs for Python errors
- Verify `requirements.txt` is correct
- Ensure `wsgi.py` exists

### "Database connection error"
- For SQLite: Should work automatically
- For PostgreSQL: Verify `DATABASE_URL` is set correctly
- Check database credentials

### "Static files not loading"
- Ensure `static/uploads/` folder exists
- Check file permissions

## Need Help?

See [DEPLOYMENT.md](../DEPLOYMENT.md) for detailed troubleshooting and configuration options.
