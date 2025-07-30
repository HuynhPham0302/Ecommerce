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
    
@address_bp.route("/addresses/<int:address_id>", methods=["GET"])
def get_address(address_id: int):
    try: 
        address = Address.query.get(address_id)

        if not address:
            return APIResponse.error(message="Address not found", status_code=400, error_code=404)
        
        address_data = address.serialize()

        return APIResponse.success(
            data=address_data,
            message="Address retrieved successfully",
            status_code=200
        )
    except Exception as e:
        return APIResponse.error(message=f"Faild to retrieve address: {e}", status_code=400, error_code=404)