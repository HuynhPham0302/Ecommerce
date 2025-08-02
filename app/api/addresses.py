from flask import Blueprint, jsonify, request
from app.models.address import Address
from app.utils.api_helpers import APIResponse
from app.extensions import db

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
@address_bp.route("/addresses", methods=["POST"])
def create_address():
    try:
        data = request.json()

        new_address = Address(
            id=data["id"],
            user_id=data["user_id"],
            address_line1=data["address_line1"],
            address_line2= data["address_line2"],
            city=data["city"],
            state_province_region= data["state_province_region"],
            postal_code=data["postal_code"],
            country=data["country"]
        )
        db.session.add(new_address)
        db.session.commit()
        return APIResponse.success(
            data=new_address.serialize(),
            message="Address created successfully",
            status_code=201
        )
    except Exception as e:
        return APIResponse.error(
            message=f"Failed to create address: {e}",
            status_code=400,
            error_code=500
        )
