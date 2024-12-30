"""
app/extentions.py

This module helps importing purposes between modules to prevent circular imports.
"""

from flask import session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()

migrate = Migrate()

mail = Mail()

login_manager = LoginManager()

def init_login_manager(app):
    login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    """
    Create login manger using flask
    
    Args:
        -int: user_id

    Returns:
        -obj: user - SQLAlchemy object of user
    """

    from app.models import Teacher, Student
    # Get user_type from session
    user_type = session.get('user_type')  # Ensure user_type is stored in session during login
    if user_type == "teacher":
        user = Teacher.query.get(int(user_id))
    elif user_type == "student":
        user = Student.query.get(int(user_id))
    else:
        user = None  # Fallback if user_type is invalid or missing
    return user