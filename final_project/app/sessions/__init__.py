# app\sessions\__init__.py

from flask import Blueprint

sessions_bp = Blueprint('sessions', __name__)


from . import routes