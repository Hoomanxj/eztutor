import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://username:password@localhost/eztutor")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

