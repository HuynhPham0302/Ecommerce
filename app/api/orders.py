from flask import Blueprint, jsonify, request
from app.models.order import Order
from app.utils.api_helpers import APIResponse
from app.extensions import db

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
    

@order_bp.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id: int):
    try:
        order = Order.query.get(order_id)
        if not order:
            return APIResponse.error(message="Order not found", status_code=400, error_code=404)
        order_data = order.serialize()

        return APIResponse.success(
            data=order_data,
            message="Order retrieved successfully",
            status_code=200
        )
    except Exception as e:
        return APIResponse.error(message=f"Failed to retrieve order: {e}", status_code=400, errpr_code=404)

@order_bp.route("/orders", methods=["POST"])
def create_order():
    try:
        data = request.json()

        new_order = Order(
            id= data["id"],
            user_id= data["user_id"],
            shipping_address_id= data["shipping_address_id"],
            order_date= data["order_data"],
            status= data["status"],
            total_amount= data["total_amount"],
            shipping_method= data["shipping_method"]
        )

        db.session.add(new_order)
        db.session.commit()

        return APIResponse.success(
            data=new_order.serialize(),
            message="Order created successfully",
            status_code=201
        )
    except Exception as e:
        return APIResponse.error(
            message=f"Failed to create order: {e}",
            status_code=400,
            error_code=500
        )