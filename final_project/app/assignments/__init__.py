# app\assignments\__init__.py

from flask import Blueprint

assignments_bp = Blueprint('assignments', __name__)


from . import routes