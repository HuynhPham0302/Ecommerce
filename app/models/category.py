from app.extensions import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    # allow query all products in a category
    products = db.relationship("Product", backref="category", lazy=True)

    # Example:
    # meat = Category.query(1) -> get category with id 1 (meat)
    # meat_products = meat.products