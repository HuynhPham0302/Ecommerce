from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.payment import Payment
from app.utils.api_helpers import APIResponse

payment_bp = Blueprint("payments", __name__)


@payment_bp.route("/payments", methods=["GET"])
# @admin_required
def get_payments():
    try:
        # from User select *
        query = Payment.query
        payments = [payment.serialize() for payment in query.all()]

        return APIResponse.success(
            data=payments, message="Payments retrieved successfully", status_code=200
        )

    except Exception as e:
        return APIResponse.error(message=f"Failed to get payments: {e}", status_code=400, error_code=500)

@payment_bp.route("/payments/<int:payment_id>", methods=["GET"])
def get_payment(payment_id:int):
    try:
        payment = Payment.query.get(payment_id)

        if not payment:
            return APIResponse.error(message="Payment not found", status_code=400, error_code=404)
        payment_data = payment.serialize()

        return APIResponse.success(
            data=payment_data,
            message="Payment retrieved successfully",
            status_code=200
        )
    except Exception as e:
        return APIResponse.error(message=f"Failed to retrieve payment: {e}", status_code=400, error_code=404)

@payment_bp.route("/payments", methods=["POST"])
def create_payment():
    try:
        data = request.get_json()

        new_payment = Payment(
            order_id=data["order_id"],
            payment_method=data["payment_method"],
            transaction_id=data["transaction_id"],
            amount=data["amount"],
            status=data["status"],
            payment_date=data["payment_date"],
        )

        db.session.add(new_payment)
        db.session.commit()

        return APIResponse.success(
            data=new_payment.serialize(),
            message="Payment added successfully",
            status_code=201,
        )
    except Exception as e:
        return APIResponse.error(
            message=f"Failed to add payment: {e}",
            status_code=400,
            error_code=500
        )
