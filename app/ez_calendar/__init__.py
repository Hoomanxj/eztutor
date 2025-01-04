"""
app\ez_calendar\__init__.py

This module handles analytical init for the blueprint.
"""

from flask import Blueprint


# Create the blueprint
calendar_bp = Blueprint('calendar', __name__)

from . import routes