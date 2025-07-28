from flask import Blueprint, jsonify, request
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