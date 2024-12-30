"""
app\course\__init__.py

This module handles analytical init for the blueprint.
"""

from flask import Blueprint


# Create the blueprint
course_bp = Blueprint('course', __name__)


from . import routes