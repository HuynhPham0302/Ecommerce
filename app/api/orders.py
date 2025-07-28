from flask import Blueprint, jsonify, request
from app.models.order import Order
from app.utils.api_helpers import APIResponse

order_bp = Blueprint("orders", __name__)

@order_bp.route("/orders", methods=["GET"])
def get_orders():
    try:
        query = Order.query
        orders = [order.serialize() for order in query.all()]
        
        return APIResponse.success(
            data=orders, message="Orders retrieved successfully", status_code=200
        )
    except Exception as e:
        return APIResponse.error(message=f"Failed to get orders: {e}", status_code=400, error_code=500)
