from flask import Blueprint, jsonify, request
from app.models.payment import Payment
from app.utils.api_helpers import APIResponse

payment_bp = Blueprint("payments", __name__)


@payment_bp.route("/payments", methods=["GET"])
# @admin_required
def get_users():
    try:
        # from User select *
        query = Payment.query
        payments = [payment.serialize() for payment in query.all()]

        return APIResponse.success(
            data=payments, message="Payments retrieved successfully", status_code=200
        )

    except Exception as e:
        return APIResponse.error(message=f"Failed to get payments: {e}", status_code=400, error_code=500)