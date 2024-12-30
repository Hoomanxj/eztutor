"""
app\course\routes.py

This module handle course view and creation.
"""
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from app.course import course_bp
from app.forms import CreateCourseForm, inviteForm
from app.models import Course, CourseWeekday
from app.extentions import db
from app.decorators import db_transaction, teacher_required
from app.queries import find_user_courses, populate_sessions
from app.choices import (
    course_type_choices, course_format_choices, grading_system_choices,
    time_choices, weekdays_choices, session_duration_choices
)
from app.emails import (
    generate_course_code, generate_course_link, course_invitation
)

@course_bp.route("/course_home", methods=["GET"])
@login_required
def course_home():
    """
    Description:
        Landing route of this page
    
    Request Parameters:
        -None
    
    Response:
        -None; renders course.html and passes page title 
    """

    # Create page title using user first name
    page_title = f"{current_user.first_name}'s courses"

    return render_template("course.html",
                           page_title=page_title)


@course_bp.route("/get_courses", methods=["GET"])
@login_required
def get_courses():
    """
    Description:
        Fetch user courses
    
    Request Parameters:
        -user_type (str)
        -user_id (int)

    Response:
        -404: Not available
        -200: success
    """

    # Fetch courses
    courses, success = find_user_courses(
        user_type=current_user.role,
        user_id=current_user.id,
        weekdays=True
    )

    # If none found
    if not success:
        return jsonify({
            "success": True,
            "message": "No courses were found"
            }), 404

    # If success
    return jsonify({
        "success": True,
        "courses": courses
        }), 200


@course_bp.route("/course_form", methods=["GET"])
@login_required
@teacher_required
def course_form():
    """
    Description:
        Render course form in frontend
    
    Request Parameters:
        -form
    
    Response:
        -200 success
        -500 exception
    
    """
    try:
        # Fetch form
        form = CreateCourseForm()

        # Render with choices
        form_html = form.render(
            course_type_choices=course_type_choices,
            course_format_choices=course_format_choices,
            grading_system_choices=grading_system_choices,
            time_choices=time_choices,
            weekdays_choices=weekdays_choices,
            session_duration_choices=session_duration_choices
        )

        # If successful
        return jsonify({
            "success": True,
            "html": form_html
            }), 200
    
    # If exception happens
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching the form: {str(e)}"
        }), 500


@course_bp.route("/submit_form", methods=["POST"])
@login_required
@teacher_required
@db_transaction
def submit_form():
    """
    Description:
        Submit form and create course
    
    Request Parameters:
        -form
        -current_user.id (id)
    
    Response:
        -400 wrong data type
        -201 new entry
        -500 exception
    """
    
    # Populate form with frontend data
    form = CreateCourseForm(formdata=request.form)

    # If validation fails
    if not form.validate_on_submit():
        return jsonify({
            "success": False,
            "message": f"Form validation Failed. Error: {str(form.errors)}"
        }), 400

    try:

        # Generate a code for the course to be used for student invites
        course_code = generate_course_code()

        # Store student email and course name for later use
        student_email = form.student_email.data
        course_name = form.name.data

        # Create a new course
        new_course = Course(
            teacher_id=current_user.id,
            name=form.name.data.lower(),
            type=form.type.data,
            format=form.format.data,
            system=form.system.data,
            description=form.description.data.lower(),
            start_date=form.start_date.data,
            start_hour=form.start_hour.data,
            number_of_session=int(form.number_of_session.data),
            session_duration=int(form.session_duration.data),
            number_of_student=int(form.number_of_student.data),
            status="ongoing",
            code=course_code,
            link=form.link.data
        )

        # Loop and add weekdays value to course
        selected_weekdays = form.weekdays.data
        for weekday in selected_weekdays:
            new_course.weekdays.append(CourseWeekday(name=weekday))

        # Add user to db
        db.session.add(new_course)

        # Flush so we can use user data here
        db.session.flush()

        # Populate sessions for course
        populate_sessions(
            user_id=current_user.id,
            course_id=new_course.id,
            start_date=new_course.start_date,
            start_hour=new_course.start_hour,
            number_of_session=new_course.number_of_session,
            day_list=selected_weekdays,
            duration=new_course.session_duration
        )
        
        # If student email was given in the form, start invitation
        if student_email:

            # Generate course invite link
            enrollment_link = generate_course_link(
            course_code=course_code)

            # Invite student
            result, success =course_invitation(
                student_email=student_email,
                course_name=course_name,
                enrollment_link=enrollment_link)
        
        # Return success
        return jsonify({
            "success": True,
            "message": "Course created successfully!"
        }), 201
    
    # If exception happens
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error creating course: {str(e)}"
        }), 500


@course_bp.route("/get_invite_form", methods=["GET"])
@login_required
@teacher_required
def get_invite_form():
    """
    Description:
        Render student invitation form
    
    Request Parameters:
        -course_id (int)
        -form
    
    Response:
        -404: not available
        -200: success
    """

    # Request course_id
    course_id = request.args.get("course_id", type=int)

    # If not passed
    if not course_id:
        return jsonify({
            "success": False,
            "message": "Missing or invalid course ID."
        }), 404
    
    # Fetch invite form
    invite_html = inviteForm().render(course_id=course_id)

    # Return success
    return jsonify({
        "success": True,
        "html": invite_html
        }), 200


@course_bp.route("/send_invitation", methods=["POST"])
@login_required
@teacher_required
def send_invitation():
    """
    Description:
        Send invitation to student
    
    Request Parameters:
        -form
        -course_id (int)

    Response:
        -404: not available
        -400: wront data type
        -500: exception
        -200: success
    """

    # Populate form with frontend data
    form = inviteForm(formdata=request.form)

    # Request course_id
    course_id = request.form.get("course_id")

    # If not passed
    if not course_id:
        return jsonify({
            "success": False,
            "message": "Missing or invalid course ID."
        }), 404

    # If form fails validation    
    if not form.validate_on_submit():
        return jsonify({
            "success": False,
            "message": f"Form validation Failed. Error: {str(form.errors)}"
        }), 400
    
    try:

        # Find users' course
        course, success = find_user_courses(
            user_type=current_user.role,
            user_id=current_user.id,
            course_id=course_id,
            weekdays=True)
        
        # If none found
        if not success or not course:
            return jsonify({
                "success": False,
                "message": "No such course found."
            }), 404
        
        # Grab course object from the list
        course = course[0]

        # Generate course invite link
        enrollment_link = generate_course_link(course_code=course["code"])

        # Invite student
        result, email_success = course_invitation(
            student_email=form.email.data,
            course_name=course["name"],
            enrollment_link=enrollment_link
        )

        # If invitation fails
        if not email_success:
            return jsonify({
                "success": False,
                "message": "Failed to send the invitation."
            }), 500
        
        # If success
        return jsonify({
            "success": True,
            "message": "Invitation sent successfully!"
        }), 200

    # If exception
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error sending invitation: {str(e)}"
        }), 500