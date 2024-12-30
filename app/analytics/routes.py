"""
app/analytics/routes.py

This module handles analytical information for student performance.
It includes: analytics_home, get_courses, get_students, get_student_courses
"""

from flask import (
    render_template, request, jsonify
)
from flask_login import login_required, current_user
from app.queries import find_student_score, find_user_courses, find_students
from app.decorators import teacher_required
from . import analytics_bp


@analytics_bp.route("/analytics_home", methods=["GET"])
@login_required
def analytics_home():
    """    
    Description:
        Landing route of this page.
    
    Request Parameters:
        -None
    
    Responses:
        -None; renders analytics.html alonside page title
       
    """

    # Create page title using user's first name
    page_title = f"{current_user.first_name.title()}'s analyitics"

    return render_template("analytics.html",
                           page_title=page_title)


@analytics_bp.route("/get_courses", methods=["GET"])
@login_required
def get_courses():
    """    
    Description:
        Fetch user's all courses

    Request Parameter:
        - user_type (str)
        - user_id (int)

    Response:
        - 200: Whether the user has courses or not

    """
    
    # Fetch courses
    courses, success = find_user_courses(user_type=current_user.role,
                                         user_id=current_user.id)
    # If they don't any courses
    if not success:
        return jsonify({
            "success": True,
            "courses": []
        }), 200
    
    # Return any courses they have
    return jsonify({
            "success": True,
            "courses": courses
        }), 200


@analytics_bp.route("/get_students", methods=["GET"])
@login_required
@teacher_required
def get_students():
    """    
    Description:
        If the user is teacher, fetch their students in a particular course.

    Request Parameters:
        -course_id (int): ID of the course
    
    Responses:
        -404: Course ID was not provided / No students found in the course
        -200: List of dictionaries with student information

    """

    # Request course ID
    course_id = request.args.get("course_id")

    # IF not available
    if not course_id:
        return jsonify({
            "success": False,
            "message": "Course ID could not be found"
        }), 404

    # Fetch students of this course
    students, success = find_students(course_id=course_id)
    
    # IF no students found in this course
    if not success:
        return jsonify({
            "success": False,
            "message": "No students in this course"
        }), 404
    
    # Return a list of students
    return jsonify({
            "success": True,
            "students": students
        }), 200


@analytics_bp.route("/get_student_scores", methods=["GET"])
@login_required
def get_student_scores():
    """
    Description:
        This route retrieves a student's scores for a specific course. 
        It requires the user to be logged in and uses the user's role to determine the behavior.
    
    Request Parameters:
        - course_id (int): ID of the course
        - student_id (int): ID of the student
        - user_type (str)
        - user_id (int)
    
    Responses:
        - 200: JSON object with success status and scores.
        - 400: Bad Request (missing or invalid parameters).
        - 403: Forbidden (invalid user role).
        - 500: Internal Server Error.

    """
    
    try:
        # Request course ID
        course_id = request.args.get("course_id", type=int)

        # If not available
        if not course_id:
            return jsonify({
                "success": False,
                "message": "Course ID could not be found"
            }), 400

        # Based on user type, decide
        if current_user.role == "student":
            student_id = current_user.id

        elif current_user.role == "teacher":
            student_id = request.args.get("student_id", type=int)
            # If user is teacher but student ID is not available
            if not student_id:
                return jsonify({
                    "success": False,
                    "message": "Student ID is required for teachers."
                }), 400
        # If user type is not teacher or student
        else:
            return jsonify({
                "success": False,
                "message": "Invalid user role."
            }), 403

        # Fetch scores from db
        scores, success = find_student_score(
            student_id=student_id,
            course_id=course_id
        )

        # If there no scores return empty
        if not success:
            return jsonify({
                "success": True,
                "scores": {}
            }), 200 

        # Send scores if found
        return jsonify({
                "success": True,
                "scores": scores
            }), 200

    # In case things go wrong
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching scores: {str(e)}"
            }), 500
