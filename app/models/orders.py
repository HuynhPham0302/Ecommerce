from app import db
from datetime import datetime
from enum import Enum
class Status(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

class Address(db.Model):
    __tablename__="orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    shipping_address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.ctcnow)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.PENDING)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    shipping_method = db.Column(db.String(50))