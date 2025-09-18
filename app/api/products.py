from flask import Blueprint, jsonify, request
from app.models.product import Product
from app.utils.api_helpers import APIResponse
from app.extensions import db

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
        return APIResponse.error(
            message=f"Failed to get products: {e}", status_code=400, error_code=500
        )


@product_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id: int):
    try:
        product = Product.query.get(product_id)

        if not product:
            return APIResponse.error(
                message="Product not found", status_code=400, error_code=404
            )
        product_data = product.serialize()

        return APIResponse.success(
            data=product_data, message="Product retrieved successfully", status_code=200
        )
    except Exception as e:
        return APIResponse.error(
            message=f"Failed to retrieve product: {e}", status_code=400, error_code=500
        )


@product_bp.route("/products", methods=["POST"])
def create_product():
    try:
        data = request.json()

        existing_product = Product.query.filter_by(name=data["name"]).first()
        if existing_product:
            return APIResponse.error(
                message="Product already exists!!!", status_code=400, error_code=500
            )

        new_product = Product(
            category_id=data["category_id"],
            name=data["name"],
            description=data["description"],
            price=data["price"],
            sku=data["sku"],
            stock_quantity=data["stock_quantity"],
            image_url=data.get("image_url"),
        )

        db.session.add(new_product)
        db.session.commit()
        return APIResponse.success(
            data=new_product.serialize(),
            message="Product created successfully",
            status_code=201,
        )
    except Exception as e:
        return APIResponse.error(
            message=f"Failed to create product: {e}", status_code=400, error_code=500
        )
