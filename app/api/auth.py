import datetime
from flask import Blueprint, current_app, request

from app.models.user import User, UserRole
from app.utils.api_helpers import APIResponse
from app.extensions import db
import bcrypt
import jwt

# api/auth
# authentication
# authorization


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user

    Request JSON:
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password": "password123",
        "phone_number": "+1234567890" (optional)
    }
    """
    try:
        data = request.json()

        exsisting_user = User.query.filter_by(email=data["email"]).first()
        if exsisting_user:
            return APIResponse.error("User with this email already exists", 409)

        hashed_password = bcrypt.hashpw(
            data["password"].encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password_hash=hashed_password,
            phone_number=data["phone_number"],
            role=UserRole.CUSTOMER,
        )

        # stash -> commit -> database

        db.session.add(user)
        db.session.commit()

        token = jwt.encode(
            {
                "user_id": user.id,
                "exp": datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return APIResponse.success(
            {"user": user.serialize(), "token": token},
            "User register successfully!!!",
            201,
        )

    except Exception as e:
        db.session.rollback()
        return APIResponse.error(f"Registration failed: {str(e)}", 500)


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login user

    Request JSON:
    {
        "email": "john@example.com",
        "password": "password123"
    }
    """

    try:
        data = request.json()
        user = User.query.filter_by(email=data["email"]).first()

        if not user:
            return APIResponse.error("Invalid email or password.", 401)

        if not bcrypt.checkpw(
            data["password"].encode("utf-8"), user.password_hash.encode("utf-8")
        ):
            return APIResponse.error("Invalid email or password", 401)

        # json web token
        token = jwt.encode(
            {
                "user_id": user.id,
                "exp": datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

        return APIResponse.success(
            {"user": user.serialize(), "token": token}, "Login successful"
        )
    except Exception as e:
        return APIResponse.error(f"Login failed: {str(e)}", 500)
