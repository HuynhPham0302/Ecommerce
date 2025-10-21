from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.product import Product
from app.utils.api_helpers import APIResponse

product_bp = Blueprint("products", __name__)


@product_bp.route("/products", methods=["GET"])
def get_products():
    """
    Get all products
    ---
    tags:
      - Products
    summary: Retrieve all products
    description: Get a list of all products in the system
    produces:
      - application/json
    responses:
      200:
        description: Products retrieved successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Products retrieved successfully"
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  category_id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: "iPhone 15 Pro"
                  description:
                    type: string
                    example: "Latest iPhone with advanced features"
                  price:
                    type: number
                    format: decimal
                    example: 999.99
                  sku:
                    type: string
                    example: "IP15PRO001"
                  stock_quantity:
                    type: integer
                    example: 50
                  image_url:
                    type: string
                    example: "https://example.com/iphone15pro.jpg"
                  created_at:
                    type: string
                    format: date-time
                    example: "2024-01-01T12:00:00Z"
                  updated_at:
                    type: string
                    format: date-time
                    example: "2024-01-01T12:00:00Z"
      500:
        description: Failed to get products
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Failed to get products: Error message"
    """
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
    """
    Get a specific product by ID
    ---
    tags:
      - Products
    summary: Retrieve a specific product
    description: Get detailed information about a product by its ID
    produces:
      - application/json
    parameters:
      - in: path
        name: product_id
        type: integer
        required: true
        description: Product ID
        example: 1
    responses:
      200:
        description: Product retrieved successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Product retrieved successfully"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                category_id:
                  type: integer
                  example: 1
                name:
                  type: string
                  example: "iPhone 15 Pro"
                description:
                  type: string
                  example: "Latest iPhone with advanced features"
                price:
                  type: number
                  format: decimal
                  example: 999.99
                sku:
                  type: string
                  example: "IP15PRO001"
                stock_quantity:
                  type: integer
                  example: 50
                image_url:
                  type: string
                  example: "https://example.com/iphone15pro.jpg"
      404:
        description: Product not found
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Product not found"
      500:
        description: Failed to retrieve product
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Failed to retrieve product: Error message"
    """
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

@product_bp.route("/products", methods=["POST"])
def create_product():
    """
    Create a new product
    ---
    tags:
      - Products
    summary: Create a new product
    description: Add a new product to the inventory
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: product_data
        description: Product information
        required: true
        schema:
          type: object
          required:
            - category_id
            - name
            - description
            - price
            - sku
            - stock_quantity
          properties:
            category_id:
              type: integer
              example: 1
              description: Category ID that the product belongs to
            name:
              type: string
              example: "iPhone 15 Pro"
              description: Product name
            description:
              type: string
              example: "Latest iPhone with advanced features"
              description: Product description
            price:
              type: number
              format: decimal
              example: 999.99
              description: Product price
            sku:
              type: string
              example: "IP15PRO001"
              description: Stock keeping unit (unique product identifier)
            stock_quantity:
              type: integer
              example: 50
              description: Available stock quantity
            image_url:
              type: string
              example: "https://example.com/iphone15pro.jpg"
              description: Product image URL (optional)
    responses:
      201:
        description: Product created successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Product created successfully"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                category_id:
                  type: integer
                  example: 1
                name:
                  type: string
                  example: "iPhone 15 Pro"
                description:
                  type: string
                  example: "Latest iPhone with advanced features"
                price:
                  type: number
                  format: decimal
                  example: 999.99
                sku:
                  type: string
                  example: "IP15PRO001"
                stock_quantity:
                  type: integer
                  example: 50
                image_url:
                  type: string
                  example: "https://example.com/iphone15pro.jpg"
      400:
        description: Product already exists or invalid data
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Product already exists!!!"
      500:
        description: Failed to create product
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Failed to create product: Error message"
    """
    try:
        data = request.get_json()

        existing_product = Product.query.filter_by(name=data["name"]).first()
        if existing_product:
            return APIResponse.error("Product already exists!!!")

        new_product = Product(
            category_id=data["category_id"],
            name=data["name"],
            description=data["description"],
            price=data["price"],
            sku=data["sku"],
            stock_quantity=data["stock_quantity"],
            image_url=data.get("image_url")
        )

        db.session.add(new_product)
        db.session.commit()
        return APIResponse.success(
            data=new_product.serialize(),
            message="Product created successfully",
            status_code=201
        )
    except Exception as e:
        return APIResponse.error(
            message=f"Failed to create product: {e}",
            status_code=400,
            error_code=500
        )
