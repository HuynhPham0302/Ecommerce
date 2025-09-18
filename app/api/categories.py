from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.category import Category
from app.utils.api_helpers import APIResponse

category_bp = Blueprint("categories", __name__)

@category_bp.route("/categories", methods=["GET"])
def get_categories():
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
