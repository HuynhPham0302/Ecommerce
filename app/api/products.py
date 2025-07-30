from flask import Blueprint, jsonify, request
from app.models.product import Product
from app.utils.api_helpers import APIResponse

product_bp = Blueprint("products", __name__)


@product_bp.route("/products", methods=["GET"])
# @admin_required
def get_products():
    try:
        # from User select *
        query = Product.query
        products = [product.serialize() for product in query.all()]

        return APIResponse.success(
            data=products, message="Products retrieved successfully", status_code=200
        )

    except Exception as e:
        return APIResponse.error(message=f"Failed to get products: {e}", status_code=400, error_code=500)

@product_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id: int):
    try:
        product = Product.query.get(product_id)

        if not product:
            return APIResponse.error(message="Product not found", status_code=400, error_code=404)
        product_data = product.serialize()

        return APIResponse.success(
            data=product_data,
            message="Product retrieved successfully",
            status_code=200
        )
    except Exception as e:
        return APIResponse.error(message=f"Failed to retrieve product: {e}", status_code=400, error_code=500)