from app.extensions import db
from datetime import datetime
from enum import Enum


class OrderStatus(Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    shipping_address_id = db.Column(
        db.Integer, db.ForeignKey("addresses.id"), nullable=False
    )
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(
        db.Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING
    )
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    shipping_method = db.Column(db.String(50))

    # Relationship
    order_items = db.relationship(
        "OrderItem", backref="order", lazy=True, cascade="all, delete-orphan"
    )
    payments = db.relationship(
        "Payment", backref="order", lazy=True, cascade="all, delete-orphan"
    )
    shipping_address = db.relationship("Address", foreign_keys=[shipping_address_id])

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "shipping_address_id": self.shipping_address_id,
            "order_date": self.order_date.isoformat() if self.order_date else None,
            "status": self.status.value if self.status else None,
            "total_amount": self.total_amount,
            "shipping_method": self.shipping_method,
        }
