# app\welcome\__init__.py

from flask import Blueprint

welcome_bp = Blueprint('welcome', __name__)


from . import routes