"""
app/helpers.py

This module hold functions and html templates for emails
"""

import os
from uuid import uuid4
from flask import url_for, current_app
from flask_login import current_user
from flask_mail import Message
from werkzeug.utils import secure_filename
from app.extentions import mail


def generate_course_code():
    """
    A helper to generate codes for each course
    
    Args:
        -None
    
    Returns:
        -str: course_code
    """

    # Create course code using uuid4
    course_code = str(uuid4())

    return course_code


def generate_course_link(course_code):
    """
    A helper to generate course-join link
    
    Args:
        -str: course_code

    Returns:
        -str: enrollment_link
    """
    # Use _external to ensure it is usable outside of app environment
    enrollment_link = url_for('auth.login_home', course_code=course_code, _external=True)

    return enrollment_link


def course_invitation(student_email, course_name, enrollment_link):
    """
    A helper to create and send course invitation email
    
    Args:
        -str: student_email
        -str: course_name
        -str: enrollment_link

    Returns:
        -"success", True: If email is sent successfully
        -"Error", False: If fails
    """

    try:
        
        # Create a Message instance
        msg = Message(
            subject=f"Invitaion to join {course_name}",
            sender="eztutorproject@gmail.com",
            recipients=[student_email]
        )

        # Form html template
        msg.html = f"""
        <p>Hello there!</p>
        <p>You have been invited to enroll in <strong>{course_name}</strong> course
        on <strong>eztutor.com</strong></p>
        <p>You can do so by clicking on <a class="text-cyan-700" href = "{enrollment_link}">Join Link</a></p>
        <p>Can't wait you to join our family of learners!</p>
        <p>Best regards,<p>
        <p class="text-amber-600">Eztutor Team</p>
        """

        # Email
        mail.send(msg)

        # If success
        return "success", True
    
    # If exception happens
    except Exception as e:
        print("Couldn't send email due to:", e)
        return f"Error attempting to send invitaion: {e}", False


def email_assignment(student, teacher, file, note):
    """
    A helper to email assignment file to teacher
    
    Args:
        -str: student - student name
        -obj: teacher - SQLAlchemy object
        -file: file - assignment attached
        -str: note - student note on assignment submission

    Returns:
        -"success" - If success
        -"Error" - If fails
    """

    filename = secure_filename(file.filename)
    upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

    try:
        file.save(upload_path)

        # Creat a Message instance
        msg = Message(
            subject=f"Assignment Submission by {current_user.first_name}",
            sender="eztutorproject@gmail.com",
            recipients=[teacher.email],
        )

        # Form html template
        msg.html = f"""
            <p>Hello dear {teacher.first_name}!<p>
            <p>{student} has submitted their assignment<p>
            <p>They also wanted to give tell you:<p>
            <p>"{note}"<p>
            <p>To score their assignment, you can go to your <strong>assignment</strong> panel and<br>
                <strong>submitted</strong> tab, or you can simply use the following link:<p>
            <a class="text-cyan-700" href="http://127.0.0.1:5000/assignment/assignment_home">Go to assignment panel</a>
            <p>Have a great day!<p>
            <p class="text-amber-600">EZtutor team<p>
        """

        with current_app.open_resource(upload_path) as f:
            msg.attach(filename, "application/octet-stream", f.read())
        
        # Email
        mail.send(msg)

        # If success
        return "success"
    
    # If exception happens
    except Exception as e:
            print("Couldn't email the assignment file to teacher")
            return f"Error attempting to send invitaion: {e}"