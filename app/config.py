import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class."""

    # Database configuration - using SQLite for development
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key for sessions and forms
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Additional configuration
    DEBUG = True
    TESTING = False
