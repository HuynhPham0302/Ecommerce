from flask import Blueprint, jsonify, request
from app.models.order_item import OrderItem
from app.utils.api_helpers import APIResponse

orderitem_bp = Blueprint("order_items", __name__)

@orderitem_bp.route("/order_items", methods=["GET"])
def get_order_items():
    try:
        query = OrderItem.query
        order_items = [order_item.serialize() for order_item in query.all()]

        return APIResponse.success(
            data=order_items, message="OrderItems retrieved successfully", status_code=200
        )
    
    except Exception as e:
        return APIResponse.error(message=f"Failed to get OrderItem: {e}", status_code=400, error_code=500)
    
@orderitem_bp.route("/order_items/<int:order_item_id>", methods=["GET"])
def get_order_item(order_item_id: int):
    try:
        order_item = OrderItem.query.get(order_item_id)

        if not order_item:
            return APIResponse.error(message="Order_item not found", status_code=400, error_code=404)
        
        order_item_data = order_item.serialize()

        return APIResponse.success(
            data=order_item_data,
            message="Order_item retrieved successfully",
            status_code=200
        )
    except Exception as e:
        return APIResponse.error(message=f"Failed to retrieve Order_item: {e}", status_code=400, error_code=404)
    