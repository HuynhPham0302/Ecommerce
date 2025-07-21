from app import db
from enum import Enum
from datetime import datetime

class Status(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    transaction_id = db.Column(db.String(255))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.PENDING)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)



