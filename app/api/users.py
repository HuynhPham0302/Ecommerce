from flask import Blueprint, jsonify, request
from app.models.user import User
from app.utils.api_helpers import APIResponse

user_bp = Blueprint("users", __name__)


@user_bp.route("/users", methods=["GET"])
# @admin_required
def get_users():
    try:
        # from User select *
        query = User.query
        items = [item.serialize() for item in query.all()]

        return APIResponse.success(
            data=items, message="Users retrieved successfully", status_code=200
        )

    except Exception as e:
        return APIResponse.error(message=f"Failed to get users: {e}", status_code=400, error_code=500)


@user_bp.route("/users/<int:user_id>", methods=["GET"])
# @admin_required
def get_user(user_id: int):
    try:
        user = User.query.get(user_id)

        if not user:
            error_response = {"success": False, "message": "User not found"}
            return jsonify(error_response), 404

        user_data = user.serialize()

        response = {
            "success": True,
            "message": "User retrieved successfully",
            "data": {"user": user_data},
        }

        return jsonify(response), 200

    except Exception as e:
        response = {
            "success": False,
            "message": f"Fail to retrieve users: {e}",
            "error_code": 500,
        }

        return jsonify(response), 400
