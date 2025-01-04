"""
app\assignments\__init__.py

This module handles analytical init for the blueprint.
"""

from flask import Blueprint


# Create the blueprint
assignment_bp = Blueprint('assignment', __name__)


from . import routes