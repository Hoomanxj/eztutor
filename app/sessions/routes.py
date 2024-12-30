# app\sessions\routes.py

from flask import (
    render_template, request, jsonify
)
from flask_login import login_required, current_user
from app.forms import UpdateSessionForm
from app.queries import find_user_courses, find_session, update_session
from app.decorators import db_transaction, teacher_required
from app.choices import (
    session_type_choices, session_status_choices, session_day_choices,
    session_duration_choices
)
from . import session_bp


@session_bp.route("/session_home", methods=["GET", "POST"])
@login_required
def session_home():
    """
    Description:
        Landing route for this page
    
    Request Parameters:
        -None
    
    Response:
        -None; renders session.html and passes page title
    """
    
    # Create page title using user first name
    page_title = f"{current_user.first_name.title()}'s sessions"
    return render_template("session.html",
                           page_title=page_title)


@session_bp.route("/get_courses", methods=["GET", "POST"])
@login_required
def get_courses():
    """
    Description:
        Fetch courses
    
    Request Parameter:
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
            weekdays=True
        )

        # If none found return empty list
        if not success:
            return jsonify({
                "success": True,
                "courses": []
            }), 200

        # If success return courses
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


@session_bp.route("/get_sessions", methods=["GET"])
@login_required
@db_transaction
def get_sessions():
    """
    Description:
        Fetch sessions
    
    Request Parameters:
        -course_id (int)
    
    Response:
        -200: whether finds courses or not
    """

    try:

        # Request course_id
        course_id = request.args.get("course_id", type=int)

        # If none found return empty list
        if not course_id:
            return jsonify({
                "success": True,
                "courses": []
            }), 200
        
        # Fetch sessions
        sessions, success = find_session(course_id)

        # If none found return empty list
        if not success:
            return jsonify({
                "success": True,
                "sessions": []
            }), 200

        # If success return sessions
        return jsonify({
                "success": True,
                "sessions": sessions
            }), 200
    
    # If exceptions happens
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching sessions: {str(e)}"
            }), 500


@session_bp.route("/get_session_info", methods=["GET"])
@login_required
def get_session_info():
    """
    Description:
        Fetch session data
    
    Request Parameter:
        -session_id (int)
    
    Response:
        -200: success
        -500: exception
    """

    try:

        # Request session id
        session_id = request.args.get("session_id", type=int)

        # Fetch session
        session, success = find_session(session_id=session_id)

        # If found return session
        if not success:
            return jsonify({
                "success": True,
                "session": session
                }), 200
        
        # Grab session object from list
        session = session[0]

        # Render session html with db data of that session
        session_html = UpdateSessionForm(obj=session).render(
            user_type=current_user.role,
            session_id=session_id,
            session_type_choices=session_type_choices,
            session_status_choices=session_status_choices,
            session_day_choices=session_day_choices,
            session_duration_choices=session_duration_choices,
        )

        # If success pass session html   
        return jsonify({
            "success": True,
            "html":session_html
            }), 200
    
    # If exception happens
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching session info: {str(e)}"
            }), 500


@session_bp.route("/update_session_info", methods=["POST"])
@login_required
@teacher_required
@db_transaction
def update_session_info():
    """
    Description:
        Update session info
    
    Request Parameters:
        -session_id (int)
        -form

    Response:
        -404: not available
        -400: wrong data type
        -200: success
        -500: exception
    """

    # Request session_id
    session_id = request.form.get("session_id")
    if not session_id:
        return jsonify({
            "success": False,
            "message": "Session ID could not be determined"
            }), 404

    # Populate form with frontend data
    form = UpdateSessionForm(formdata=request.form)

    # If form fails validation
    if not form.validate_on_submit():
        return jsonify({
        "success": False,
        "message": f"Form validation Failed. Error: {str(form.errors)}"
        }), 400 
        
    try:

        # Update session info
        result, success = update_session(
            session_id=session_id,
            session_type=form.type.data or None,
            session_status=form.status.data or None,
            session_date=form.date.data or None,
            session_day=form.day.data or None,
            session_duration=form.duration.data or None,
            session_description=form.description.data or None
        )

        # If no such session found
        if result == "no_session":
            return jsonify({
                "success": False,
                "message": "Session was not found"
                }), 404
        
        # If success
        elif result == "success":
            return jsonify({
                "success": True,
                "message": "Successfully updated session info"
                }), 200
        
        # If things go wrong
        else:
            return jsonify({
                "success": False,
                "message": result
                }), 500
    # If exception happens   
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error updating session: {str(e)}"
            }), 500
