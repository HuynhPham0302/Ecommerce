from .addresses import address_bp
from .auth import auth_bp
from .categories import category_bp
from .order_items import orderitem_bp
from .orders import order_bp
from .payments import payment_bp
from .products import product_bp
from .users import user_bp

__all__ = [
    address_bp,
    auth_bp,
    category_bp,
    orderitem_bp,
    order_bp,
    payment_bp,
    product_bp,
    user_bp,
]
