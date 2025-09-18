#!/usr/bin/env python3

"""
Database Seeding Script for E-commerce Application
This script populates the database with sample data for development and testing.
"""

import os
import sys
from datetime import datetime
from decimal import Decimal

import bcrypt

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from app import create_app
from app.extensions import db
from app.models.address import Address
from app.models.category import Category
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.payment import Payment, PaymentStatus
from app.models.product import Product
from app.models.user import User, UserRole


def hash_password(password: str) -> str:
    """Generate bcrypt hash for a password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def clear_database():
    """Clear all data from the database"""
    print("Clearing existing data...")
    
    try:
        # Order matters due to foreign key constraints
        db.session.query(Payment).delete()
        db.session.query(OrderItem).delete()
        db.session.query(Order).delete()
        db.session.query(Address).delete()
        db.session.query(Product).delete()
        db.session.query(Category).delete()
        db.session.query(User).delete()
        
        db.session.commit()
        print("Database cleared successfully!")
    except Exception as e:
        print(f"Error clearing database: {e}")
        db.session.rollback()
        # If clearing fails, try to drop and recreate tables
        print("Attempting to recreate tables...")
        db.drop_all()
        db.create_all()
        print("Tables recreated successfully!")


def seed_users():
    """Create sample users with properly hashed passwords"""
    print("Creating users...")

    # Default password for all seed users (can be different in production)
    default_password = "password123"

    users = [
        User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password_hash=hash_password(default_password),
            phone_number="+1234567890",
            role=UserRole.ADMIN,
        ),
        User(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            password_hash=hash_password(default_password),
            phone_number="+1234567891",
            role=UserRole.CUSTOMER,
        ),
        User(
            first_name="Alice",
            last_name="Johnson",
            email="alice.johnson@example.com",
            password_hash=hash_password(default_password),
            phone_number="+1234567892",
            role=UserRole.CUSTOMER,
        ),
        User(
            first_name="Bob",
            last_name="Wilson",
            email="bob.wilson@example.com",
            password_hash=hash_password(default_password),
            phone_number="+1234567893",
            role=UserRole.CUSTOMER,
        ),
    ]

    for user in users:
        db.session.add(user)

    db.session.commit()
    print(f"Created {len(users)} users with password: '{default_password}'")
    return users


def seed_categories():
    """Create sample categories"""
    print("Creating categories...")
    
    categories = [
        Category(
            name="Electronics",
            description="Electronic devices and gadgets"
        ),
        Category(
            name="Clothing",
            description="Fashion and apparel"
        ),
        Category(
            name="Books",
            description="Books and educational materials"
        ),
        Category(
            name="Home & Garden",
            description="Home improvement and gardening supplies"
        ),
        Category(
            name="Sports & Outdoors",
            description="Sports equipment and outdoor gear"
        )
    ]
    
    for category in categories:
        db.session.add(category)
    
    db.session.commit()
    print(f"Created {len(categories)} categories")
    return categories


def seed_products(categories):
    """Create sample products"""
    print("Creating products...")
    
    products = [
        # Electronics
        Product(
            category_id=categories[0].id,
            name="MacBook Air M2",
            description="Apple MacBook Air 13-inch with M2 chip, 8GB RAM, 256GB SSD",
            price=Decimal("1199.99"),
            sku="MBA-M2-256",
            stock_quantity=25,
            image_url="https://example.com/macbook-air.jpg"
        ),
        Product(
            category_id=categories[0].id,
            name="iPhone 15 Pro",
            description="Apple iPhone 15 Pro 128GB - Titanium Blue",
            price=Decimal("999.99"),
            sku="IP15P-128-TB",
            stock_quantity=50,
            image_url="https://example.com/iphone-15-pro.jpg"
        ),
        Product(
            category_id=categories[0].id,
            name="Samsung Galaxy S24",
            description="Samsung Galaxy S24 256GB - Phantom Black",
            price=Decimal("849.99"),
            sku="SGS24-256-PB",
            stock_quantity=30,
            image_url="https://example.com/galaxy-s24.jpg"
        ),
        
        # Clothing
        Product(
            category_id=categories[1].id,
            name="Nike Air Max 270",
            description="Nike Air Max 270 Running Shoes - Black/White",
            price=Decimal("149.99"),
            sku="NAM270-BW-10",
            stock_quantity=100,
            image_url="https://example.com/nike-air-max.jpg"
        ),
        Product(
            category_id=categories[1].id,
            name="Levi's 501 Jeans",
            description="Levi's 501 Original Fit Jeans - Dark Blue",
            price=Decimal("79.99"),
            sku="L501-DB-32",
            stock_quantity=75,
            image_url="https://example.com/levis-501.jpg"
        ),
        
        # Books
        Product(
            category_id=categories[2].id,
            name="Clean Code",
            description="Clean Code: A Handbook of Agile Software Craftsmanship by Robert Martin",
            price=Decimal("29.99"),
            sku="CC-ROBERT-HC",
            stock_quantity=200,
            image_url="https://example.com/clean-code.jpg"
        ),
        Product(
            category_id=categories[2].id,
            name="The Pragmatic Programmer",
            description="The Pragmatic Programmer: Your Journey to Mastery",
            price=Decimal("34.99"),
            sku="TPP-JOURNEY-PB",
            stock_quantity=150,
            image_url="https://example.com/pragmatic-programmer.jpg"
        ),
        
        # Home & Garden
        Product(
            category_id=categories[3].id,
            name="Dyson V15 Detect",
            description="Dyson V15 Detect Cordless Vacuum Cleaner",
            price=Decimal("749.99"),
            sku="DV15D-CORD",
            stock_quantity=15,
            image_url="https://example.com/dyson-v15.jpg"
        ),
        
        # Sports & Outdoors
        Product(
            category_id=categories[4].id,
            name="Yeti Rambler 20oz",
            description="Yeti Rambler 20oz Tumbler with MagSlider Lid",
            price=Decimal("39.99"),
            sku="YR20-MAG-SS",
            stock_quantity=80,
            image_url="https://example.com/yeti-rambler.jpg"
        )
    ]
    
    for product in products:
        db.session.add(product)
    
    db.session.commit()
    print(f"Created {len(products)} products")
    return products


def seed_addresses(users):
    """Create sample addresses"""
    print("Creating addresses...")
    
    addresses = [
        Address(
            user_id=users[1].id,  # Jane Smith
            address_line1="123 Main Street",
            address_line2="Apt 4B",
            city="New York",
            state_province_region="NY",
            postal_code="10001",
            country="USA"
        ),
        Address(
            user_id=users[1].id,  # Jane Smith - second address
            address_line1="456 Oak Avenue",
            city="Brooklyn",
            state_province_region="NY",
            postal_code="11201",
            country="USA"
        ),
        Address(
            user_id=users[2].id,  # Alice Johnson
            address_line1="789 Pine Road",
            city="Los Angeles",
            state_province_region="CA",
            postal_code="90210",
            country="USA"
        ),
        Address(
            user_id=users[3].id,  # Bob Wilson
            address_line1="321 Elm Street",
            city="Chicago",
            state_province_region="IL",
            postal_code="60601",
            country="USA"
        )
    ]
    
    for address in addresses:
        db.session.add(address)
    
    db.session.commit()
    print(f"Created {len(addresses)} addresses")
    return addresses


def seed_orders(users, addresses, products):
    """Create sample orders"""
    print("Creating orders...")
    
    orders = [
        Order(
            user_id=users[1].id,  # Jane Smith
            shipping_address_id=addresses[0].id,
            status=OrderStatus.DELIVERED,
            total_amount=Decimal("1379.98"),
            shipping_method="Standard Shipping"
        ),
        Order(
            user_id=users[2].id,  # Alice Johnson
            shipping_address_id=addresses[2].id,
            status=OrderStatus.PROCESSING,
            total_amount=Decimal("64.98"),
            shipping_method="Express Shipping"
        ),
        Order(
            user_id=users[3].id,  # Bob Wilson
            shipping_address_id=addresses[3].id,
            status=OrderStatus.PENDING,
            total_amount=Decimal("789.98"),
            shipping_method="Standard Shipping"
        )
    ]
    
    for order in orders:
        db.session.add(order)
    
    db.session.commit()
    print(f"Created {len(orders)} orders")
    return orders


def seed_order_items(orders, products):
    """Create sample order items"""
    print("Creating order items...")
    
    order_items = [
        # Order 1 - Jane Smith
        OrderItem(
            order_id=orders[0].id,
            product_id=products[0].id,  # MacBook Air M2
            quantity=1,
            price_per_unit=products[0].price
        ),
        OrderItem(
            order_id=orders[0].id,
            product_id=products[3].id,  # Nike Air Max 270
            quantity=1,
            price_per_unit=products[3].price
        ),
        
        # Order 2 - Alice Johnson
        OrderItem(
            order_id=orders[1].id,
            product_id=products[5].id,  # Clean Code
            quantity=1,
            price_per_unit=products[5].price
        ),
        OrderItem(
            order_id=orders[1].id,
            product_id=products[6].id,  # The Pragmatic Programmer
            quantity=1,
            price_per_unit=products[6].price
        ),
        
        # Order 3 - Bob Wilson
        OrderItem(
            order_id=orders[2].id,
            product_id=products[7].id,  # Dyson V15 Detect
            quantity=1,
            price_per_unit=products[7].price
        ),
        OrderItem(
            order_id=orders[2].id,
            product_id=products[8].id,  # Yeti Rambler
            quantity=1,
            price_per_unit=products[8].price
        )
    ]
    
    for item in order_items:
        db.session.add(item)
    
    db.session.commit()
    print(f"Created {len(order_items)} order items")
    return order_items


def seed_payments(orders):
    """Create sample payments"""
    print("Creating payments...")
    
    payments = [
        Payment(
            order_id=orders[0].id,
            payment_method="Credit Card",
            amount=orders[0].total_amount,
            status=PaymentStatus.COMPLETED,
            transaction_id="txn_123456789"
        ),
        Payment(
            order_id=orders[1].id,
            payment_method="PayPal",
            amount=orders[1].total_amount,
            status=PaymentStatus.COMPLETED,
            transaction_id="txn_987654321"
        ),
        Payment(
            order_id=orders[2].id,
            payment_method="Credit Card",
            amount=orders[2].total_amount,
            status=PaymentStatus.PENDING,
            transaction_id="txn_456789123"
        )
    ]
    
    for payment in payments:
        db.session.add(payment)
    
    db.session.commit()
    print(f"Created {len(payments)} payments")
    return payments


def main():
    """Main seeding function"""
    print("🌱 Starting database seeding...")
    print("=" * 50)
    
    # Create Flask app and database tables
    app = create_app()
    
    with app.app_context():
        # Drop and recreate all tables to ensure clean state
        print("Recreating database tables...")
        # db.drop_all()
        db.create_all()
        print("Tables created successfully!")
        
        # Clear any existing data (safety measure)
        clear_database()
        
        # Seed data in order (respecting foreign key constraints)
        users = seed_users()
        categories = seed_categories()
        products = seed_products(categories)
        addresses = seed_addresses(users)
        orders = seed_orders(users, addresses, products)
        order_items = seed_order_items(orders, products)
        payments = seed_payments(orders)
        
        print("=" * 50)
        print("🎉 Database seeding completed successfully!")
        print("\nSummary:")
        print(f"  - {len(users)} users created")
        print(f"  - {len(categories)} categories created")
        print(f"  - {len(products)} products created")
        print(f"  - {len(addresses)} addresses created")
        print(f"  - {len(orders)} orders created")
        print(f"  - {len(order_items)} order items created")
        print(f"  - {len(payments)} payments created")
        print("\nYou can now test your application with this sample data!")


if __name__ == "__main__":
    main()
