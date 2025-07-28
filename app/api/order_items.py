from flask import Blueprint, jsonify, request
from app.models.order_item import OrderItem
from app.utils.api_helpers import APIResponse

orderitem_bp = Blueprint("orderitems", __name__)

@orderitem_bp.route("/orderitems", methods=["GET"])
def get_orderitems():
    try:
        query = OrderItem.query
        orderitems = [orderitem.serialize() for orderitem in query.all()]

        return APIResponse.success(
            data=orderitems, message="OrderItems retrieved successfully", status_code=200
        )
    
    except Exception as e:
        return APIResponse.error(message=f"Failed to get OrderItem: {e}", status_code=400, error_code=500)