from flask import Flask, render_template, redirect, url_for, flash, request, make_response, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from models import db, User, Product
from forms import RegistrationForm, LoginForm, ProductForm, SettingsForm
from config import Config
from seed import seed_db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database initialization function
def init_db():
    """Initialize database - runs on first app context creation"""
    with app.app_context():
        # Create all tables if they don't exist
        db.create_all()
        
        # Only seed if no users exist
        if User.query.first() is None:
            seed_db()
            print("Database initialized and seeded with sample data.")
        else:
            print("Database already initialized.")

# Initialize database on app startup (works with both dev and production)
with app.app_context():
    try:
        db.create_all()
        # Check if database needs seeding
        if User.query.first() is None:
            seed_db()
    except Exception as e:
        print(f"Database initialization error: {e}")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    products = Product.query.filter_by(user_id=current_user.id).all()
    total_products = len(products)
    today = datetime.today().date()
    active_products = len([p for p in products if p.expiry_date and p.expiry_date >= today])
    expired_products = len([p for p in products if p.expiry_date and p.expiry_date < today])
    expiring_soon = len([p for p in products if p.expiry_date and (p.expiry_date - today).days <= 30 and p.expiry_date >= today])
    total_value = sum(p.price for p in products)
    upcoming = [p for p in products if p.expiry_date and (p.expiry_date - today).days <= 30 and p.expiry_date >= today]
    expired = [p for p in products if p.expiry_date and p.expiry_date < today]
    
    # Calculate average warranty duration
    warranty_durations = [p.warranty_duration for p in products if p.warranty_duration]
    avg_warranty_duration = sum(warranty_durations) / len(warranty_durations) if warranty_durations else 0
    
    # Calculate most valuable product
    max_value = max([p.price for p in products]) if products else 0
    
    return render_template('dashboard.html', upcoming=upcoming, expired=expired, total_products=total_products, active_products=active_products, expired_products=expired_products, expiring_soon=expiring_soon, total_value=total_value, avg_warranty_duration=avg_warranty_duration, max_value=max_value)

@app.route('/products')
@login_required
def products():
    query = request.args.get('q', '')
    category_filter = request.args.get('category', '')
    base_query = Product.query.filter_by(user_id=current_user.id)

    if query:
        base_query = base_query.filter(
            (Product.name.contains(query) | Product.brand.contains(query) | Product.category.contains(query))
        )

    if category_filter:
        base_query = base_query.filter(Product.category == category_filter)

    products = base_query.all()
    # Get existing categories for filter dropdown
    existing_categories = db.session.query(Product.category).filter_by(user_id=current_user.id).distinct().all()
    categories = [cat[0] for cat in existing_categories]
    return render_template('products.html', products=products, query=query, category_filter=category_filter, categories=categories, datetime=datetime)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    # Get existing categories for suggestions
    existing_categories = db.session.query(Product.category).filter_by(user_id=current_user.id).distinct().all()
    categories = [cat[0] for cat in existing_categories]
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            brand=form.brand.data,
            category=form.category.data,
            purchase_date=form.purchase_date.data,
            warranty_duration=form.warranty_duration.data,
            price=form.price.data,
            receipt=form.receipt.data,
            user_id=current_user.id
        )
        product.calculate_expiry()
        if form.receipt_file.data:
            file = form.receipt_file.data
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{current_user.id}_receipt_{filename}")
                file.save(file_path)
                product.receipt_path = f"{current_user.id}_receipt_{filename}"
        if form.product_image.data:
            file = form.product_image.data
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{current_user.id}_image_{filename}")
                file.save(file_path)
                product.product_image = f"{current_user.id}_image_{filename}"
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_product.html', form=form, categories=categories)

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if product.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    form = ProductForm(obj=product)
    # Get existing categories for suggestions
    existing_categories = db.session.query(Product.category).filter_by(user_id=current_user.id).distinct().all()
    categories = [cat[0] for cat in existing_categories]
    if form.validate_on_submit():
        # Handle file uploads first
        if form.receipt_file.data:
            file = form.receipt_file.data
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{current_user.id}_receipt_{filename}")
                file.save(file_path)
                product.receipt_path = f"{current_user.id}_receipt_{filename}"
        if form.product_image.data:
            file = form.product_image.data
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{current_user.id}_image_{filename}")
                file.save(file_path)
                product.product_image = f"{current_user.id}_image_{filename}"
        
        # Update other fields
        product.name = form.name.data
        product.brand = form.brand.data
        product.category = form.category.data
        product.purchase_date = form.purchase_date.data
        product.warranty_duration = form.warranty_duration.data
        product.price = form.price.data
        product.receipt = form.receipt.data
        
        product.calculate_expiry()
        db.session.commit()
        flash('Product updated successfully.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_product.html', form=form, product=product, categories=categories)

@app.route('/delete_product/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    if product.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))

    # Delete associated files
    if product.receipt_path:
        receipt_path = os.path.join('static', 'uploads', product.receipt_path)
        if os.path.exists(receipt_path):
            os.remove(receipt_path)

    if product.product_image:
        image_path = os.path.join('static', 'uploads', product.product_image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    return redirect(url_for('products', q=query))

@app.route('/export_csv')
@login_required
def export_csv():
    import csv
    from io import StringIO
    products = Product.query.filter_by(user_id=current_user.id).all()
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Name', 'Brand', 'Category', 'Purchase Date', 'Warranty Duration', 'Price', 'Expiry Date'])
    for product in products:
        writer.writerow([
            product.name,
            product.brand,
            product.category,
            product.purchase_date.strftime('%Y-%m-%d'),
            product.warranty_duration,
            product.price,
            product.expiry_date.strftime('%Y-%m-%d')
        ])
    output = si.getvalue()
    si.close()
    response = make_response(output)
    response.headers['Content-Disposition'] = 'attachment; filename=products.csv'
    response.headers['Content-type'] = 'text/csv'
    return response

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        # Check current password
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('settings'))

        # Update email if changed
        if form.email.data != current_user.email:
            # Check if email is already taken
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user and existing_user.id != current_user.id:
                flash('Email address is already in use.', 'danger')
                return redirect(url_for('settings'))
            current_user.email = form.email.data

        # Update password if provided
        if form.new_password.data:
            current_user.set_password(form.new_password.data)

        db.session.commit()
        flash('Settings updated successfully.', 'success')
        return redirect(url_for('settings'))

    # Pre-populate form with current data
    form.email.data = current_user.email

    # Calculate account statistics
    total_products = Product.query.filter_by(user_id=current_user.id).count()
    account_age_days = (datetime.utcnow() - current_user.created_at).days if current_user.created_at else 0

    return render_template('settings.html', form=form, total_products=total_products, account_age_days=account_age_days)

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    # Check if the file belongs to the current user
    product = Product.query.filter(
        (Product.receipt_path == filename) | (Product.product_image == filename),
        Product.user_id == current_user.id
    ).first()

    if not product:
        flash('File not found or access denied.', 'danger')
        return redirect(url_for('dashboard'))

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Run Flask development server
    app.run(debug=True)