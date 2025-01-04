"""
app\ez_calendar\routes.py

This module handles calendar routes.
"""
from datetime import datetime
from flask import (render_template, jsonify, request
)
from flask_login import login_required, current_user
from app.queries import find_schedule, find_class_schedule, find_all_schedule
from app.decorators import db_transaction
from app.forms import AddTaskForm
from app.models import CustomTask
from app.extentions import db
from . import calendar_bp


@calendar_bp.route("/calendar_home", methods=["GET", "POST"])
@login_required
def calendar_home():
    """
    Description:
        Landing page for this page
    
    Request Parameters:
        -None
    
    Response:
        -None; renders calendar.html and passes page title
    """

    # Create page title using user first name
    page_title= f"{current_user.first_name.title()}'s calendar"

    return render_template("calendar.html",
                           page_title=page_title)


@calendar_bp.route("/get_custom_schedule", methods=["GET", "POST"])
@login_required
def get_custom_schedule():
    """
    Description:
        Fetch the custome schedule of a user
    
    Request Parameters:
        -user_type (str)
        -user_id (id)

    Response:
        -200: whether finds custom schedule or not
        -500: exception
    """
    
    try:

        # Fetch custom schedule
        custom_schedule, success = find_schedule(
            user_type=current_user.role,
            user_id=current_user.id
        )

        # If none found return empty list
        if not success:
            return jsonify({
                "success": True,
                "custom_schedule": []
                }), 200
        
        # If success return custom schedule
        return jsonify({
            "success": True,
            "custom_schedule": custom_schedule
            }), 200
    
    # If exception happens
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching custom schedule: {str(e)}"
        }), 500


@calendar_bp.route("/get_class_schedule", methods=["GET", "POST"])
@login_required
def get_class_schedule():
    """
    Description:
        Fetch the class schedule of a user
        
    Request Parameters:
        -user_type (str)
        -user_id (id)
    
    Response:
        -200: whether finds class schedule or not
        -500: exception
    """
    try:

        # Fetch class schedule
        class_schedule, success = find_class_schedule(
            user_type=current_user.role,
            user_id=current_user.id
        )

        # If none found return empty list
        if not success:
            return jsonify({
                "success": True,
                "class_schedule": []
                }), 200

        # If success return class schedule
        return jsonify({
        "success": True,
        "class_schedule": class_schedule
        }), 200
    
    # If exception happens
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching class schedule: {str(e)}"
        }), 500


@calendar_bp.route("/get_all_schedule", methods=["GET"])
@login_required
def get_all_schedule():
    """
    Description:
        Fetch the class schedule of a user
    
    Request Parameters:
        -user_type (str)
        -user_id (id)
    
    Response:
        -200: whether finds schedule or not
        -500: exception
    """
    try:

        # Fetch schedule of any type
        all_schedule, success = find_all_schedule(
            user_type=current_user.role,
            user_id=current_user.id
        )

        # If none found return empty list
        if not success:
            return jsonify({
                "success": True,
                "all_schedule": []
                }), 200

        # If success return all schedule
        return jsonify({
        "success": True,
        "all_schedule": all_schedule
        }), 200

    # If exception happens
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching all schedule: {str(e)}"
        }), 500


@calendar_bp.route("/get_task_form", methods=["GET"])
@login_required
def get_task_form():
    """
    Description:
        Fetch task form and pass to frontend
    
    Request Parameters:
        -form
    
    Response:
        -200: success
        -500: exception
    """
    try:

        # Fetch form
        form = AddTaskForm()
        form_html = form.render()

        # Return success
        return jsonify({
            "success": True,
            "html": form_html
            }), 200
    
    # If exception happens
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching custom task form: {str(e)}"
        }), 500


@calendar_bp.route("/add_task", methods=["POST"])
@login_required
@db_transaction
def add_task():
    """
    Description:
        Add the custom task to db
    
    Request Parameters:
        -form
        -date (date)
    
    Response:
        -404: not available
        -400: wrong data type
        -200: success
        -500: exception
    """

    # Fetch form
    form = AddTaskForm(request.form)

    # Request date
    date = request.form.get("date")

    # If not passed
    if not date:
        return jsonify({
                "success": True,
                "message": "Date for the custom task could not be determined"
                }), 404
    
    # If form validation fails
    if not form.validate_on_submit():
        return jsonify({
                "success": True,
                "message": f"Form validation failed. Error: {str(form.errors)}"
                }), 400
    try:

        # Create new task
        new_task = CustomTask(
            teacher_id=current_user.id if current_user.role == "teacher" else None,
            student_id=current_user.id if current_user.role == "student" else None,
            task=form.task.data.lower(),
            date=datetime.strptime(date, '%Y-%m-%d').date(),
            time_from=form.time_from.data,
            time_to=form.time_to.data
        )

        # Add new task to db
        db.session.add(new_task)

        # If success
        return jsonify({
            "success": True,
            "message": "Custom task successfully created"
            }), 200
    
    # If excepetion happens
    except Exception as e:    
        return jsonify({
            "success": False,
            "message": f"Error creating new task: {str(e)}"
            }), 500
    
    