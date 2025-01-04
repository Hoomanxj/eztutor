"""
app/dashboard/routes.py

This module handle dashboard routes.
"""
from datetime import datetime
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from app.decorators import teacher_required
from app.queries import (
    find_user_courses, find_all_schedule, find_session,
    find_student_score, find_students
    )
from . import dashboard_bp


@dashboard_bp.route("/dashboard_home", methods=["GET"])
@login_required
def dashboard_home():
    """
    Description:
        Landing route for this page
    
    Request Parameters:
        -None
    
    Response:
        -None; renders dashboard.html and passes page title
    """

    # Create page title using user first name
    page_title = f"{current_user.first_name.title()}`s Dashboard"
    
    return render_template("dashboard.html",
                           page_title=page_title)


@dashboard_bp.route("/get_courses", methods=["GET"])
@login_required
def get_courses():
    """
    Description:
        Get all courses
    
    Request Parameters:
        -user_type (str)
        -user_id (int)
    
    Response:
        -200: whether finds courses or not
        -500: exception
    """

    try:

        # Fetch courses
        courses, success = find_user_courses(
            user_type=current_user.role,
            user_id=current_user.id,
            weekdays=True,
        )

        # If none found
        if not success:
            return jsonify({
                "success": True,
                "message": "No courses were found",
                "courses": []
                }), 200
        
        # Return list of courses
        return jsonify({
            "success": True,
            "courses": courses
            }), 200
    
    # If exception happens
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching courses: {str(e)}"
            }), 500


@dashboard_bp.route("/get_students", methods=["GET"])
@login_required
@teacher_required
def get_students():
    """
    Description:
        Fetch teacher's students - Only for teacher
    
    Request Parameters:
        -course_id (int)
    
    Response:
        -404: not available
        -200: success
        -500: exception
    """
    try:

        # Request course_id
        course_id = request.args.get("course_id")

        # If not passed
        if not course_id:
            return jsonify({
                "success": False,
                "message": "Course ID could not be found"
            }), 404

        # Fetch students
        students, success = find_students(course_id=course_id)

        # If none found
        if not success:
            return jsonify({
                "success": False,
                "message": "No students in this course"
            }), 404
        
        # If success return list of students
        return jsonify({
                "success": True,
                "students": students
            }), 200
    
    # If exception happens
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching students: {str(e)}"
        }), 500


@dashboard_bp.route("/get_schedule", methods=["GET"])
@login_required
def get_schedule():
    """
    Description:
        Get user's schedule
    
    Request Parameters:
        -user_type (str)
        -user_id (int)
        -today (date)
    
    Response:
        -200: whether found schedule or not
        -500: exception
    """

    try:

        # Fetch today's schedule
        schedule, success = find_all_schedule(
            user_type=current_user.role,
            user_id=current_user.id,
            today=datetime.today().date()
        )

        # If none found
        if not success or not schedule:
            return jsonify({
                "success": True,
                "message": "Nothing scheduled",
                "schedule": []
                }), 200

        # If success return schedule
        return jsonify({
            "success": True,
            "schedule": schedule
            }), 200
    
    # If exception happens
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching schedule: {str(e)}"
            }), 500


@dashboard_bp.route("/get_upcoming_session", methods=["GET"])
@login_required
def get_upcoming_session():
    """
    Description:
        Fetch the upcoming session
    
    Request Parameters:
        -user_type (str)
        -user_id (int)
        -today (date)
    
    Response:
        -200: whether finds upcoming session or not
        -500: exception
    """

    try:

        # Fetch session and its course
        session, course, success = find_session(
            user_type=current_user.role,
            user_id=current_user.id,
            today=datetime.today().date()
        )

        # If none found
        if not success:
            return jsonify({
                "success": True,
                "message": "No session or course was found",
                "session": [],
                "course": []
                }), 200
        
        # JSONify session data
        session = {
            "id": session.id,
            "number": session.number,
            "type": session.type,
            "status": session.status,
            "date": session.date.strftime('%Y-%m-%d'),
            "day": session.day,
            "start_hour": session.start_hour.strftime('%H:%M'),
            "duration": session.duration,
            "description": session.description
        }

        # JSONify course data
        course = {
            "id": course.id,
            "name": course.name,
            "type": course.type,
            "format": course.format,
            "system": course.system,
            "description": course.description,
            "link": course.link
        }

        # If success return session and course array
        return jsonify({
            "success": True,
            "session": session,
            "course": course
            }), 200
    
    # If exception happens
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching data for upcoming session: {str(e)}"
            }), 500
    

@dashboard_bp.route("/get_student_scores", methods=["GET"])
@login_required
def get_student_scores():
    """
    Description:
        Fetch student scores based on category and each tag
    
    Request Parameters:
        -course_id (int)
        -student_id (int)

    Response:
        -404: not available
        -200: whether finds score or not
        -500: exception
    """
    
    try:
        
        # Request course_id
        course_id = request.args.get("course_id", type=int)

        # If not passed
        if not course_id:
            return jsonify({
                "success": False,
                "message": "Course ID could not be found"
            }), 404

        # Request student_id
        student_id = (
            current_user.id if current_user.role == "student"
            else request.args.get("student_id", type=int)
        )

        # Fetch student score
        scores, success = find_student_score(
            student_id=student_id,
            course_id=course_id
        )

        # If none found return empty list
        if not success:
            return jsonify({
                "success": True,
                "scores": []
            }), 200
        
        # If success return scores
        return jsonify({
                "success": True,
                "scores": scores
            }), 200
    
    # If exception happens
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching scores: {str(e)}"
            }), 500