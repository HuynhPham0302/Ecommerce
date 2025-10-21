import datetime

import bcrypt
import jwt
from flasgger import swag_from
from flask import Blueprint, current_app, request

from app.extensions import db
from app.models.user import User, UserRole
from app.utils.api_helpers import APIResponse

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: user_data
        required: true
        schema:
          type: object
          required: [first_name, last_name, email, password]
          properties:
            first_name:
              type: string
              example: "John"
            last_name:
              type: string
              example: "Doe"
            email:
              type: string
              example: "john.doe@example.com"
            password:
              type: string
              example: "password123"
            phone_number:
              type: string
              example: "+1234567890"
    responses:
      201:
        description: User registered successfully
      409:
        description: User already exists
      500:
        description: Registration failed
    """
    try:
        data = request.get_json()

        exsisting_user = User.query.filter_by(email=data["email"]).first()
        if exsisting_user:
            return APIResponse.error("User with this email already exists", 409)

        hashed_password = bcrypt.hashpw(
            data["password"].encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password_hash=hashed_password,
            phone_number=data["phone_number"],
            role=UserRole.CUSTOMER
        )

        db.session.add(user)
        db.session.commit()

        token = jwt.encode(
            {
                "user_id": user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return APIResponse.success(
            {
                "user": user.serialize(),
                "token": token
            },
            "User register successfully!!!",
            201
        )

    except Exception as e:
        db.session.rollback()
        return APIResponse.error(f"Registration failed: {str(e)}", 500)


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    """
    Login user
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: login_data
        required: true
        schema:
          type: object
          required: [email, password]
          properties:
            email:
              type: string
              example: "john.doe@example.com"
            password:
              type: string
              example: "password123"
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
      500:
        description: Login failed
    """

    try:
        data = request.get_json()
        user = User.query.filter_by(email=data["email"]).first()

        if not user:
            return APIResponse.error("Invalid email or password.", 401)

        # Convert stored password hash back to bytes for bcrypt comparison
        if not bcrypt.checkpw(data["password"].encode("utf-8"), user.password_hash.encode("utf-8")):
            return APIResponse.error("Invalid email or password", 401)

        # json web token
        token = jwt.encode(
            {
                "user_id": user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

        return APIResponse.success(
            {
                "user": user.serialize(),
                "token": token
            },
            "Login successful"
        )
    except Exception as e:
        return APIResponse.error(f"Login failed: {str(e)}", 500)
