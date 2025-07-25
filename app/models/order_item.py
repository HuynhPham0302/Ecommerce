from app.extensions import db

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"),nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_per_unit = db.Column(db.Numeric(10, 2), nullable=False)

    __table_args__ = (db.UniqueConstraint('order_id', 'product_id', name='uk_order_product'),)