"""
app/decorators.py

This module holds decorators used for routes
"""

from functools import wraps
from flask import current_app, redirect, url_for, flash
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from app.extentions import db


def db_transaction(func):
    """ Handle transactions for data integrity on db """

    @wraps(func)
    def wrapper(*args, **kwargs):

        try:
            result = func(*args, **kwargs)
            db.session.commit()
            return result
        
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error in {func.__name__}: {str(e)}")
            return "Database operation failed", 500
        finally:
            db.session.remove()
    return wrapper


def teacher_required(func):
    """ Ensures only teacher can access a route """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role != "teacher":
            flash("This is only for teachers!", "danger")
            return redirect(url_for("welcome.welcome"))
        return func(*args, **kwargs)
    return wrapper


def student_required(func):
    """ Ensures only student can access a route """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role != "student":
            flash("This is only for students!", "danger")
            return redirect(url_for("welcome.welcome"))
        return func(*args, **kwargs)
    return wrapper




