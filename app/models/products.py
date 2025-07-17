from datetime import datetime
from app import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    sku = db.Column(db.String(100), nullable=False, unique=True)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.Datetime, default=datetime.utcnow)
    updated_at = db.Column(db.Datetime, default=datetime.utcnow, onupdate=datetime.utcnow)