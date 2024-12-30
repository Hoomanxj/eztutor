"""
app\sessions\__init__.py

This module handles analytical init for the blueprint.
"""

from flask import Blueprint

# Create the blueprint
analytics_bp = Blueprint('analytics', __name__)


from . import routes