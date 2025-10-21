from flasgger import swag_from
from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.category import Category
from app.utils.api_helpers import APIResponse

category_bp = Blueprint("categories", __name__)

@category_bp.route("/categories", methods=["GET"])
def get_categories():
    """
    Get all categories
    ---
    tags:
      - Categories
    summary: Retrieve all categories
    description: Get a list of all product categories
    produces:
      - application/json
    responses:
      200:
        description: Categories retrieved successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Categories retrieved successfully"
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: "Electronics"
                  description:
                    type: string
                    example: "Electronic devices and gadgets"
                  created_at:
                    type: string
                    format: date-time
                    example: "2024-01-01T12:00:00Z"
                  updated_at:
                    type: string
                    format: date-time
                    example: "2024-01-01T12:00:00Z"
      500:
        description: Failed to get categories
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Failed to get categories: Error message"
    """
    try:
        query = Category.query
        categories = [category.serialize() for category in query.all()]

        return APIResponse.success(
            data=categories, message="Categories retrieved successfully", status_code=200
        )
    except Exception as e:
        return APIResponse.error(message=f"Failed to get categories: {e}", status_code=400, error_code=500)

@category_bp.route("/categories/<int:category_id>", methods=["GET"])
def get_category(category_id: int):
    """
    Get a specific category by ID
    ---
    tags:
      - Categories
    summary: Retrieve a specific category
    description: Get detailed information about a category by its ID
    produces:
      - application/json
    parameters:
      - in: path
        name: category_id
        type: integer
        required: true
        description: Category ID
        example: 1
    responses:
      200:
        description: Category retrieved successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Category retrieved successfully"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                name:
                  type: string
                  example: "Electronics"
                description:
                  type: string
                  example: "Electronic devices and gadgets"
      404:
        description: Category not found
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Category not found"
      500:
        description: Failed to retrieve category
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Failed to retrieve category: Error message"
    """
    try:
        category = Category.query.get(category_id)
        if not category:
            return APIResponse.error(message="Category not found", status_code=400, error_code=404)
        category_data = category.serialize()

        return APIResponse.success(
            data=category_data,
            message="Category retrieved successfully",
            status_code=200
        )
    except Exception as e:
        return APIResponse.error(message=f"Failed to retrieve category: {e}", status_code=400, error_code=404)

@category_bp.route("/categories", methods=["POST"])
def create_category():
    """
    Create a new category
    ---
    tags:
      - Categories
    summary: Create a new product category
    description: Add a new category for organizing products
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: category_data
        description: Category information
        required: true
        schema:
          type: object
          required:
            - name
            - description
          properties:
            name:
              type: string
              example: "Electronics"
              description: Category name
            description:
              type: string
              example: "Electronic devices and gadgets"
              description: Category description
    responses:
      201:
        description: Category created successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Category created successfully"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                name:
                  type: string
                  example: "Electronics"
                description:
                  type: string
                  example: "Electronic devices and gadgets"
      500:
        description: Failed to create category
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Failed to create category: Error message"
    """
    try:
        data = request.get_json()

        new_category = Category(name=data["name"], description=data["description"])

        db.session.add(new_category)
        db.session.commit()
        return APIResponse.success(
            data=new_category.serialize(),
            message="Category created successfully",
            status_code=201
        )
    except Exception as e:
        return APIResponse.error(
            message=f"Failed to create category: {e}",
            status_code=400,
            error_code=500
        )
