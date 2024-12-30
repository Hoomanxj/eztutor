"""
app\sessions\__init__.py

This module handles analytical init for the blueprint.
"""

from flask import Blueprint


# Create the blueprint
session_bp = Blueprint('session', __name__)


from . import routes