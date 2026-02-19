# Digital Warranty & Product Receipt Record Manager

A Flask-based web application for managing digital warranties and product receipts with user authentication, file uploads, and database integration.

## Features

- 🔐 User Authentication (registration and login)
- 📤 Receipt & Invoice Upload (PDF and image formats)
- 🧾 Product & Warranty Management
- 📱 Responsive UI with Tailwind CSS
- 🔎 Search Functionality
- ✏️ Record Maintenance
- ⏰ Warranty Tracking

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd DigitalWarranty
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser and go to `http://127.0.0.1:5000/`

## Usage

1. Register a new account or login with existing credentials.
2. Upload receipts/invoices and add product details.
3. View and manage your warranty records on the dashboard.
4. Search products by name or brand.
5. Edit or delete records as needed.

## Technologies Used

- Flask
- SQLAlchemy
- Flask-Login
- Flask-WTF
- Tailwind CSS
- SQLite (default database)


## Users
 - sachin@gmail.com / password
 - mouli@gmail.com / password
 - admin@gmail.com / admin123

## Deployment

### Quick Deployment on Render 🚀

Deploy this application for free on [Render.com](https://render.com):

1. Go to [render.com](https://render.com) and sign in with GitHub
2. Create a new Web Service → Select this repository
3. Render auto-detects Python and will config automatically
4. Add environment variables (SECRET_KEY, FLASK_ENV=production)
5. Deploy! Your app will be live in seconds

📖 Detailed instructions: See [DEPLOYMENT.md](DEPLOYMENT.md)

### Local Development

```bash
python app.py
```

### Production with Gunicorn

```bash
gunicorn wsgi:app
```

## Project Structure

```
DigitalWarranty/
├── app.py              # Main Flask application
├── wsgi.py            # WSGI entry point for production
├── config.py          # Configuration & paths
├── models.py          # Database models
├── forms.py           # Forms
├── seed.py            # Sample data seeding
├── instance/          # Persistent database folder
├── static/            # CSS, uploads, images
├── templates/         # HTML templates
├── requirements.txt   # Dependencies
├── Procfile          # Deployment config
├── render.yaml       # Render configuration
└── DEPLOYMENT.md     # Detailed deployment guide
```

## Features

- ✅ User authentication with secure passwords
- ✅ Warranty tracking with expiry dates
- ✅ Receipt/invoice upload support
- ✅ Professional responsive UI (Tailwind CSS)
- ✅ Search and filtering
- ✅ Database persistence across restarts
- ✅ Production-ready deployment

## Support

For deployment help, see [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.