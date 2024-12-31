"""
app/config.py

This module handles the configuration of the app.
"""

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Base configuration for the app.
    """

    # App start config
    SECRET_KEY = os.getenv("SECRET_KEY", "default_key")  # Default fallback for development

    # Database configuration
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "").replace("mysql://", "mysql+pymysql://")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://username:password@localhost/eztutor")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

    # Email service configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "eztutorproject@gmail.com")  # Read from .env for flexibility
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "default_password")  # Read from .env for security
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "eztutorproject@gmail.com")  # Read from .env

class DevelopmentConfig(Config):
    """
    Development-specific configuration.
    """
    DEBUG = True

class ProductionConfig(Config):
    """
    Production-specific configuration.
    """
    DEBUG = False
