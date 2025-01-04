"""
app\welcome\__init__.py

This module handles welcome init for the blueprint.
"""

from flask import Blueprint


# Create welcome blueprint
welcome_bp = Blueprint('welcome', __name__)


from . import routes