from models import db, User, Product
from datetime import datetime
import os
from PIL import Image, ImageDraw, ImageFont
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def create_placeholder_image(text, filename, category=None):
    # Create different types of placeholder images based on category
    colors = {
        'Electronics': ('#E8F4FD', '#1E88E5'),  # Light blue, blue
        'Kitchen Appliances': ('#FFF3E0', '#FF9800'),  # Light orange, orange
        'Furniture': ('#F3E5F5', '#9C27B0'),  # Light purple, purple
        'Clothing': ('#E8F5E8', '#4CAF50'),  # Light green, green
        'Books': ('#FFF8E1', '#FFC107'),  # Light yellow, amber
        'Sports Equipment': ('#FFEBEE', '#F44336'),  # Light red, red
    }

    bg_color, text_color = colors.get(category, ('lightgray', 'black'))

    # Create image with random size variation
    width = random.randint(250, 350)
    height = random.randint(200, 300)

    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Try to use a better font
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        except:
            font = ImageFont.load_default()

    # Word wrap the text
    words = text.split()
    lines = []
    current_line = ""
    max_width = width - 40

    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    # Draw text centered
    total_text_height = len(lines) * 30
    y_start = (height - total_text_height) / 2

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) / 2
        y = y_start + i * 30
        draw.text((x, y), line, fill=text_color, font=font)

    # Add some decorative elements based on category
    if category == 'Electronics':
        # Draw some circuit-like lines
        for _ in range(5):
            x1 = random.randint(10, width-10)
            y1 = random.randint(10, height-10)
            x2 = random.randint(10, width-10)
            y2 = random.randint(10, height-10)
            draw.line((x1, y1, x2, y2), fill=text_color, width=1)
    elif category == 'Kitchen Appliances':
        # Draw some steam/food icons
        draw.ellipse((width-50, 20, width-20, 50), fill=text_color)
    elif category == 'Sports Equipment':
        # Draw some motion lines
        for i in range(3):
            x = width - 30 - i*10
            draw.line((x, height//2 - 20, x, height//2 + 20), fill=text_color, width=2)

    img.save(filename)

def create_receipt_pdf(filename, receipt_data):
    """Create a PDF receipt with the given data"""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title = Paragraph(f"<b>RECEIPT - {receipt_data['receipt_number']}</b>", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))

    # Store info
    store_info = f"""
    <b>Store:</b> Digital Warranty Store<br/>
    <b>Date:</b> {receipt_data['date']}<br/>
    <b>Customer:</b> {receipt_data['customer']}
    """
    story.append(Paragraph(store_info, styles['Normal']))
    story.append(Spacer(1, 12))

    # Product info
    product_info = f"""
    <b>Product:</b> {receipt_data['product_name']}<br/>
    <b>Brand:</b> {receipt_data['brand']}<br/>
    <b>Category:</b> {receipt_data['category']}<br/>
    <b>Price:</b> ₹{receipt_data['price']:,.2f}<br/>
    <b>Warranty:</b> {receipt_data['warranty_months']} months
    """
    story.append(Paragraph(product_info, styles['Normal']))
    story.append(Spacer(1, 12))

    # Footer
    footer = Paragraph("<i>Thank you for your purchase!</i>", styles['Italic'])
    story.append(footer)

    doc.build(story)

def seed_db():
    # Create sample users
    users_data = [
        {'email': 'test@example.com', 'password': 'password'},
        {'email': 'user2@example.com', 'password': 'password'},
        {'email': 'admin@example.com', 'password': 'admin123'}
    ]

    users = []
    for user_data in users_data:
        user = User.query.filter_by(email=user_data['email']).first()
        if not user:
            user = User(email=user_data['email'])
            user.set_password(user_data['password'])
            db.session.add(user)
            db.session.commit()  # Commit each user to get id
        users.append(user)

    # Sample products
    products_data = [
        {
            'name': 'iPhone 15 Pro',
            'brand': 'Apple',
            'category': 'Electronics',
            'purchase_date': datetime(2025, 6, 1),
            'warranty_duration': 24,
            'price': 99999.17,  # 1199.99 USD * 83.33 INR
            'receipt': 'INV-2025-001',
            'user_index': 0
        },
        {
            'name': 'Samsung Galaxy S24',
            'brand': 'Samsung',
            'category': 'Electronics',
            'purchase_date': datetime(2025, 7, 15),
            'warranty_duration': 24,
            'price': 74999.17,  # 899.99 USD * 83.33 INR
            'receipt': 'INV-2025-002',
            'user_index': 0
        },
        {
            'name': 'MacBook Air M3',
            'brand': 'Apple',
            'category': 'Electronics',
            'purchase_date': datetime(2025, 8, 1),
            'warranty_duration': 36,
            'price': 108332.17,  # 1299.99 USD * 83.33 INR
            'receipt': 'INV-2025-003',
            'user_index': 0
        },
        {
            'name': 'Samsung Refrigerator',
            'brand': 'Samsung',
            'category': 'Kitchen Appliances',
            'purchase_date': datetime(2024, 12, 1),
            'warranty_duration': 12,
            'price': 100000.00,  # 1200.00 USD * 83.33 INR
            'receipt': 'INV-2024-045',
            'user_index': 0
        },
        {
            'name': 'Keurig Coffee Maker',
            'brand': 'Keurig',
            'category': 'Kitchen Appliances',
            'purchase_date': datetime(2025, 10, 10),
            'warranty_duration': 6,
            'price': 12499.50,  # 150.00 USD * 83.33 INR
            'receipt': 'INV-2025-067',
            'user_index': 0
        },
        {
            'name': 'Instant Pot',
            'brand': 'Instant Pot',
            'category': 'Kitchen Appliances',
            'purchase_date': datetime(2025, 9, 20),
            'warranty_duration': 12,
            'price': 7499.17,  # 89.99 USD * 83.33 INR
            'receipt': 'INV-2025-089',
            'user_index': 0
        },
        {
            'name': 'Wooden Dining Table',
            'brand': 'IKEA',
            'category': 'Furniture',
            'purchase_date': datetime(2025, 1, 1),
            'warranty_duration': 60,
            'price': 41665.00,  # 500.00 USD * 83.33 INR
            'receipt': 'INV-2025-101',
            'user_index': 0
        },
        {
            'name': 'Office Chair',
            'brand': 'Herman Miller',
            'category': 'Furniture',
            'purchase_date': datetime(2025, 3, 15),
            'warranty_duration': 120,
            'price': 100000.00,  # 1200.00 USD * 83.33 INR
            'receipt': 'INV-2025-102',
            'user_index': 0
        },
        {
            'name': 'Nike Running Shoes',
            'brand': 'Nike',
            'category': 'Clothing',
            'purchase_date': datetime(2025, 11, 1),
            'warranty_duration': 12,
            'price': 10832.17,  # 129.99 USD * 83.33 INR
            'receipt': 'INV-2025-201',
            'user_index': 1
        },
        {
            'name': 'Levi\'s Jeans',
            'brand': 'Levi\'s',
            'category': 'Clothing',
            'purchase_date': datetime(2025, 10, 5),
            'warranty_duration': 6,
            'price': 6665.17,  # 79.99 USD * 83.33 INR
            'receipt': 'INV-2025-202',
            'user_index': 1
        },
        {
            'name': 'Python Crash Course Book',
            'brand': 'No Starch Press',
            'category': 'Books',
            'purchase_date': datetime(2025, 12, 1),
            'warranty_duration': 0,  # Books don't have warranty
            'price': 2499.17,  # 29.99 USD * 83.33 INR
            'receipt': 'INV-2025-301',
            'user_index': 1
        },
        {
            'name': 'Yoga Mat',
            'brand': 'Manduka',
            'category': 'Sports Equipment',
            'purchase_date': datetime(2025, 8, 20),
            'warranty_duration': 24,
            'price': 9999.17,  # 119.99 USD * 83.33 INR
            'receipt': 'INV-2025-401',
            'user_index': 2
        },
        {
            'name': 'Dumbbells Set',
            'brand': 'Bowflex',
            'category': 'Sports Equipment',
            'purchase_date': datetime(2025, 7, 10),
            'warranty_duration': 60,
            'price': 16665.17,  # 199.99 USD * 83.33 INR
            'receipt': 'INV-2025-402',
            'user_index': 2
        },
        {
            'name': 'Treadmill',
            'brand': 'NordicTrack',
            'category': 'Sports Equipment',
            'purchase_date': datetime(2025, 5, 1),
            'warranty_duration': 120,
            'price': 208332.17,  # 2499.99 USD * 83.33 INR
            'receipt': 'INV-2025-403',
            'user_index': 2
        },
        {
            'name': 'Bluetooth Speaker',
            'brand': 'JBL',
            'category': 'Electronics',
            'purchase_date': datetime(2025, 9, 15),
            'warranty_duration': 12,
            'price': 6665.17,  # 79.99 USD * 83.33 INR
            'receipt': 'INV-2025-501',
            'user_index': 2
        }
    ]

    for i, prod_data in enumerate(products_data):
        user = users[prod_data['user_index']]
        product = Product(
            name=prod_data['name'],
            brand=prod_data['brand'],
            category=prod_data['category'],
            purchase_date=prod_data['purchase_date'],
            warranty_duration=prod_data['warranty_duration'],
            price=prod_data['price'],
            receipt=prod_data['receipt'],
            user_id=user.id
        )
        product.calculate_expiry()

        # Create placeholder image
        image_filename = f"{user.id}_image_{i}.png"
        image_path = os.path.join('static', 'uploads', image_filename)
        create_placeholder_image(prod_data['name'], image_path, prod_data['category'])
        product.product_image = image_filename

        # Create receipt PDF
        receipt_filename = f"{user.id}_receipt_{i}.pdf"
        receipt_path = os.path.join('static', 'uploads', receipt_filename)

        receipt_data = {
            'receipt_number': prod_data['receipt'],
            'date': prod_data['purchase_date'].strftime('%Y-%m-%d'),
            'customer': user.email,
            'product_name': prod_data['name'],
            'brand': prod_data['brand'],
            'category': prod_data['category'],
            'price': prod_data['price'],
            'warranty_months': prod_data['warranty_duration']
        }

        create_receipt_pdf(receipt_path, receipt_data)
        product.receipt_path = receipt_filename

        db.session.add(product)
    db.session.commit()
    print("Database seeded with sample data.")