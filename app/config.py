"""
app/config.py

This module handles configuration of app
"""

from dotenv import load_dotenv
import os

load_dotenv()
class Config:
    """
    Set configuration of app
    """

    # App start config
    SECRET_KEY = os.getenv("SECRET_KEY", "default_key")
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://username:password@localhost/eztutor")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "").replace("mysql://", "mysql+pymysql://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email attachment folder
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

    # Email service
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'eztutorproject@gmail.com'
    MAIL_PASSWORD = 'lgea htjb lvdc iqvf' # app password
    MAIL_DEFAULT_SENDER = 'eztutorproject@gmail.com'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False