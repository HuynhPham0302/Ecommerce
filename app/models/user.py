from app import db
from enum import Enum
from datetime import datetime


class UserRole(Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Comlumn(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20))
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    addresses = db.relationship("Address", backref="user", lazy=True, cascade='all, delete-orphan')
    orders = db.relationship("Order", backref="user", lazy=True)

    # user = User.query.get(1)
    # user_orders = user.orders  # Returns list of Order objects
    # bidirectional relationship

