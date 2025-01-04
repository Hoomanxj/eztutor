"""
app\authentication\__init__.py

This module handles analytical init for the blueprint.
"""

from flask import Blueprint


# Create the blueprint
auth_bp = Blueprint('auth', __name__)


from . import routes