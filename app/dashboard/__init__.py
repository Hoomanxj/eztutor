"""
app/dashboard/__init__.py

This module handles analytical init for the blueprint.
"""

from flask import Blueprint


# Create the blueprint
dashboard_bp = Blueprint('dashboard', __name__)

from . import routes
