"""
Script to manually reseed the database
Run this with: python reseed.py
"""

import os
import sys
from app import app, db
from models import User, Product
from seed import seed_db

if __name__ == '__main__':
    with app.app_context():
        print("Clearing existing data...")
        # Drop all tables
        db.drop_all()
        print("✓ Database cleared")
        
        # Recreate tables
        db.create_all()
        print("✓ Tables created")
        
        # Seed with new data
        seed_db()
        print("✓ Database reseeded with product-named image files")
        
        # Show what was created
        users = User.query.all()
        products = Product.query.all()
        print(f"\n✓ Created {len(users)} users and {len(products)} products")
        print("\nProduct image files created:")
        for product in products:
            print(f"  - {product.product_image}")
