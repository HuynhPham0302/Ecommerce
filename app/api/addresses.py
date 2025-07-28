from flask import Blueprint, jsonify, request
from app.models.address import Address
from app.utils.api_helpers import APIResponse

address_bp = Blueprint("addresses", __name__)

@address_bp.route("/addresses", methods=["GET"])
def get_addresses():
    try:
        query = Address.query
        addresses = [address.serialize() for address in query.all()]

        return APIResponse.success(
            data=addresses, message="Address retrieved successfully", status_code=200
        )
    except Exception as e:
        return APIResponse.error(message=f"Failed to get addresses: {e}", status_code=400, error_code=500)