# app\registry\__init__.py

from flask import Blueprint

registery_bp = Blueprint('registry', __name__)


from . import routes