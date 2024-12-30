
"""
app\auth\routes.py

This module handles both login and registeration for loing.html and registry.html
"""
from flask import (
    render_template, request, redirect, url_for, session, jsonify,
)
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash
from app.auth import auth_bp
from app.forms import RegisterUserForm, LoginForm
from app.models import Teacher, Student
from app.queries import email_pass_check, add_student,unique_email_check
from app.extentions import db
from app.decorators import db_transaction
from app.choices import (
    user_type_choices, gender_choices,
    education_level_choices
)

@auth_bp.route("/login_home", methods=["GET", "POST"])
def login_home():
    """
    Description:
        Landing route for login.html
    
    Request Parameter:
        -course_code (str) (optional)
    
    Response:
        -None; renders login.html and course code, if available
    """

    # If course code is embedded in URL grab it
    course_code = request.args.get("course_code")

    return render_template("login.html", course_code=course_code)


@auth_bp.route("/get_login_form", methods=["GET"])
def get_login_form():
    """
    Description:
        Fetch login form
    
    Request Parameter:
        -form
        -user_type_choices (list)

    Response:
        -200 success    
    """
    
    # Fetch login form with user_type_choices
    form_html = LoginForm().render(
        user_type_choices=user_type_choices
        )

    # Return success    
    return jsonify({
        "success": True,
        "html": form_html
        }), 200


@auth_bp.route("/log_user_in", methods=["POST"])
def log_user_in():
    """
    Description:
        Log user in
    
    Request Parameters:
        -course_code (str) (optional)
        -form

    Response:
        -404: not available
        -403: bad request
        -400: wrong data type
        -200: success
        -500: exception
    """

    # If course code is embedded in URL
    course_code = request.form.get("course_code")

    # Populate form with frontend data
    form = LoginForm(formdata=request.form)

    # If form fails validation
    if not form.validate_on_submit():
        return jsonify({
            "success": False,
            "message": f"Form validation Failed. Error: {str(form.errors)}"
        }), 400
    
    try:
        
        # Check cridentials
        user, success = email_pass_check(
            user_type=form.user_type.data,
            user_email=form.email.data,
            user_password=form.password.data
        )

        # If fails the check
        if not success:
            return jsonify({
                "success": False,
                "message": user
                }), 403
        
        # Need this to be passed to data_loader() to find the correct table
        session["user_type"] = form.user_type.data

        # Log user in via flask login_user function
        login_user(user)

        # If there is a course code (user is invited by a teacher)
        if isinstance(course_code, str) and course_code != "None":
            course_name, success = add_student(
                student_id=current_user.id,
                course_code=course_code
            )
            
            # If successfully added student to course
            if success == "success":
                return jsonify({
                    "success": True,
                    "message": f"You were successfully added to {course_name}"
                }), 200
            
            # If student is already added to the course
            elif success == "enrolled":
                return jsonify({
                    "success": True,
                    "message": f"You are already enrolled in {course_name}"
                }), 200
            
            # If fails to add student
            elif success == "failed":
                return jsonify({
                    "success": False,
                    "message": f"Failed to enroll in {course_name}"
                }), 500
            
        # Log user in and send them to dashboard
        return jsonify({
            "success": True,
            "redirect_url": url_for('dashboard.dashboard_home')
            }), 200
    
    # If exception happens
    except Exception as e:

        return jsonify({
            "success": False,
            "message": f"Error loging in: {str(e)}"
            }), 500


@auth_bp.route("/register_home", methods=["GET"])
def register_home():
    """
    Description:
        Landing route for register.html
    
    Request Parameters:
        -course_code (str) (optional)

    Response:
        -None; renders registry.html and course_code, if embedded in URL
    
    """

    # Request course code if embedded in URL
    course_code = request.args.get("course_code")

    return render_template("registry.html", course_code=course_code)


@auth_bp.route("/get_register_form", methods=["GET"])
def get_register_form():
    """
    Description:
        Fetch registry form
    
    Request Parameter:
        -user_type (str)
        -form

    Response:
        -404: not available
        -200: success    

    """

    # Request user type set by radio buttons
    user_type = request.args.get("user_type")

    # If not passed
    if not user_type:
        return jsonify({
            "success": False,
            "message": "User type could not be determined to load the proper form"
        }), 404

    # Pass the form
    form_html = RegisterUserForm().render(
        user_type=user_type,
        gender_choices=gender_choices,
        education_level_choices=education_level_choices
        )
    # If success
    return jsonify({
        "success": True,
        "html": form_html
        }), 200


@auth_bp.route("/register_user", methods=["POST"])
@db_transaction
def register_user():
    """
    Description:
        Register the user
    
    Request Parameter:
        -course_code (str) (optional)
        -user_type (str)

    Response:
        -404: not available
        -403: bad request
        -200: success
        -500: exception
    """

    # Request course code if embedded in URL
    course_code = request.form.get("course_code")

    # Populate form with frontend data
    form = RegisterUserForm(formdata=request.form)

    # Request user type
    user_type = request.args.get("user_type")

    # If not passed
    if not user_type:
        return jsonify({
            "success": False,
            "message": "User type could not be determined for registration"
        }), 404
    
    # Choose the table (model) to store user data based on user user type
    if user_type == "teacher":
        model = Teacher
    elif user_type == "student":
        model = Student
    
    # If user type is not teacher or student
    else:
        return jsonify({
            "success": False,
            "message": f"{user_type} is an invalid user type"
            }), 403

    # If form fails validation
    if not form.validate_on_submit():
        return jsonify({
            "success": False,
            "message": f"Form validation Failed. Error: {str(form.errors)}"
        }),
    
    try:
        
        # Create a new user
        new_user = model(
            first_name=form.first_name.data.lower(),
            last_name=form.last_name.data.lower(),
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data or None,
            email=form.email.data,
            cell=form.cell.data,
            country=form.country.data.lower(),
            city=form.city.data.lower(),
            address=form.address.data.lower(),
            education_level=form.education_level.data,
            field_of_study=form.field_of_study.data.lower(),
            native_language=form.native_language.data,
            password_hash=generate_password_hash(form.password.data),
        )

        # Choose between learned/taught language based on user type
        if user_type == "teacher":
            new_user.teaching_language=form.teaching_language.data
        elif user_type == "student":
            new_user.learning_language=form.learning_language.data

        # Check if email is already being used for the user type table
        # User will still be able to create an account for the other user type
        check = unique_email_check(
                user_type=user_type,
                email=form.email.data,
            )
        
        # If email is being used
        if not check:
            return jsonify({
                "success": False,
                "message": f"This email is already connected to a {user_type} account"
                }), 400

        # Add user to db        
        db.session.add(new_user)

        # Check cridentials
        user, success = email_pass_check(
            user_type=user_type,
            user_email=form.email.data,
            user_password=form.password.data
        )

        # If fails
        if not success:
            return jsonify({
                "success": False,
                "message": "Email and password don't match"
                }), 400
        
        # Send user to login if successful
        return jsonify({
            "success": True,
            "redirect_url": url_for('auth.login_home', course_code=course_code)
            }), 200
    
    # If exception happens
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error registering: {str(e)}"
            }), 500


@auth_bp.route("/log_user_out", methods=["GET", "POST"])
def log_user_out():
    """
    Description:
        logout user
    
    Request parameter:
        -None
    
    Response:
        -None; redirects to welcome page
    """

    # Clear the session for the next user
    session.pop('user_type', None)

    # Log user out from flask login
    logout_user()
    
    return redirect(url_for("welcome.welcome"))
