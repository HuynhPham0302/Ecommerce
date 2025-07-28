from flask import Blueprint, jsonify, request
from app.models.product import Product
from app.utils.api_helpers import APIResponse

product_bp = Blueprint("products", __name__)


@product_bp.route("/products", methods=["GET"])
# @admin_required
def get_users():
    try:
        # from User select *
        query = Product.query
        products = [product.serialize() for product in query.all()]

        return APIResponse.success(
            data=products, message="Products retrieved successfully", status_code=200
        )

    except Exception as e:
        return APIResponse.error(message=f"Failed to get products: {e}", status_code=400, error_code=500)