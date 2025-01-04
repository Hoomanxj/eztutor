"""
app\assignments\routes.py

This module handles assignment routes. All operations for creating,
submitting, scoring and viewing assignments. 
"""

from datetime import datetime
from flask import (
    render_template, request, jsonify                 
)
from werkzeug.datastructures import CombinedMultiDict
from flask_login import login_required, current_user
from app.extentions import db
from app.models import Assignment, Score
from app.decorators import (
    teacher_required, student_required, db_transaction,
)
from app.forms import (
    dynamic_create_assignment, CreateAssignmentForm, SubmitAssignmentForm,
    dynamic_score_assignment, ScoreAssignmentForm
)
from app.queries import (
    find_user_courses, find_user_assignments, find_score_choices, add_assignment_score,
    update_assignment_status, find_students_teacher, find_session_by_number, find_tag,
    add_to_assignment, find_students, find_assignment_category
)
from app.forms import assignment_category_choices
from app.emails import email_assignment
from . import assignment_bp


@assignment_bp.route("/assignment_home", methods=["GET"])
@login_required
def assignment_home():
    """    
    Description:
        Landing route of this page.
    
    Request Parameters:
        -None
    
    Response:
        -None; renders assignment.html and page title
    """

    # Create page title using user's first name
    page_title = f"{current_user.first_name.title()}'s assignments"
    return render_template("assignment.html",
                           page_title=page_title)


@assignment_bp.route("/get_courses", methods=["GET"])
@login_required
def get_courses():
    """    
    Description:
        Fetch all user's courses using user type and ID.
    
    Request Parameter:
        -user_type (str)
        -user_id (int)
    
    Response:
        -200: Whether there are courses or not

    """

    # Fetch courses
    courses, success = find_user_courses(
        user_type=current_user.role,
        user_id=current_user.id)
    
    # If nothing found
    if not success:
        return jsonify({
            "success": True,
            "courses": []
            }), 200
    
    # Return courses
    return jsonify({
            "success": True,
            "courses": courses
            }), 200


@assignment_bp.route("/get_students", methods=["GET"])
@login_required
@teacher_required
def get_students():
    """
    Description:
        Fetch students of the selected course
    
    Request Parameters:
        -course_id(int,query)

    Response:
        -404: Course ID was not passed
        -200: Whether there are students or not

    """

    # Request course ID
    course_id = request.args.get("course_id", type=int)

    # If not given
    if not course_id:
        return jsonify({
            "success": False,
            "message": "Course ID was not found to fetch students"
        }), 404
    
    # Fetch students
    students, success = find_students(course_id=course_id)

    # If none available
    if not success:
        return jsonify({
            "success": False,
            "message": "There are no students in this course",
            "students": []
        }), 200
    
    # Return all students
    return jsonify({
        "success": True,
        "students": students
    }), 200


@assignment_bp.route("/get_assignments", methods=["GET"])
@login_required
def get_assignments():
    """
    Description:
        Fetch user's assignments
    
    Request parameters:
        -course_id (int)
        -student_id (int)
        -user_type (str)
        -user_id (int)

    Response:
        -404: Course ID or student ID not passed
        -200: Whether assignments found or not
    """

    # Request course and student ID
    course_id = request.args.get("course_id", type=int)
    student_id = request.args.get("student_id", type=int)

    # If not passed
    if not course_id:
        return jsonify({
            "success": False,
            "message": "Course ID was not found to fetch assignments"
        }), 404
    
    # If user is teacher but no student ID was passed
    if current_user.role == "teacher" and not student_id:
        return jsonify({
            "success": False,
            "message": "Student ID was not found to fetch assignments"
        }), 404

    # If teacher is making the query
    if current_user.role == "teacher":
        user_type = "student"
        user_id = student_id

    # If student is making the query
    elif current_user.role == "student":
        user_type = current_user.role
        user_id = current_user.id

    # Fetch assignments
    assignments, success = find_user_assignments(
        user_type=user_type,
        user_id=user_id,
        course_id=course_id
    )

    # IF none found
    if not success:
        return jsonify({
            "success": True,
            "assignments": []
        }), 200
    
    # JSONify assignment objects found
    assignments = [{
        "id": assignment.id,
        "status": assignment.status,
        "category": assignment.category,
        "score": assignment.score,
        "start_date": assignment.start_date.strftime('%Y-%m-%d')
        if assignment.start_date else None,
        "end_date": assignment.end_date.strftime('%Y-%m-%d')
        if assignment.end_date else None,
        "pending_stamp": assignment.pending_stamp.strftime('%Y-%m-%d')
        if assignment.pending_stamp else None,
        "submitted_stamp": assignment.submitted_stamp.strftime('%Y-%m-%d')
        if assignment.submitted_stamp else None,
        "scored_stamp": assignment.scored_stamp.strftime('%Y-%m-%d')
        if assignment.scored_stamp else None,
    } for assignment in assignments]
    
    # Return all assignments
    return jsonify({
        "success": True,
        "assignments": assignments
    }), 200


@assignment_bp.route("/get_form", methods=["GET"])
@login_required
def get_form():
    """
    Description:
        Send form to front-end based on request. all types are: create,
        submit and score.
    
    Request Parameter:
        -course_id (int)
        -form_type (str)
        -assignment_id (int)
        -category_choices (list)
        -pairs (list): score/lable pairs
        -system_type (str): scoring system used
    
    Response:
        -404: Request params not passed
        -403: Invalid form type
        -200: form html passed to front end
    
    """

    course_id = request.args.get("course_id")
    form_type = request.args.get("form_type")
    assignment_id = request.args.get("assignment_id")

    if current_user.role == "teacher" and not course_id:
            return jsonify({
                "success": False,
                "message": "Course ID could not be determined to fetch the form"
            }), 404
    
    if not form_type:
            return jsonify({
                "success": False,
                "message": "Form type could not be determined"
            }), 404

    if form_type != "create" and not assignment_id:
        return jsonify({
            "success": False,
            "message": "Assignment ID could not be determined"
        }), 404
    
    form_html = ""

    if form_type == "create":
        form = dynamic_create_assignment()
        form_html = form.render(category_choices=assignment_category_choices)

    elif form_type == "submit":
        form_html = SubmitAssignmentForm().render()

    elif form_type == "score":
        form, pairs, system_type = dynamic_score_assignment(
            course_id=course_id,
            assignment_id=assignment_id)
        form_html = form.render(pairs=pairs,
                                system_type=system_type)

    else:
        return jsonify({
            "success": False,
            "message": "Invalid form type"
        }), 403

    return jsonify({
        "success": True, 
        "html": form_html
        }), 200


@assignment_bp.route("/create_assignment", methods=["POST"])
@login_required
@teacher_required
@db_transaction
def create_assignment():
    """
    Description:
        Validate and store new assignment - only teacher 
    
    Request Parameters:
        -form: form data
        -form.category.choices (str)
        -course_id (int)
        -session_id (int)
        -assignment_id (int)
    
    
    Response:
        -404: not available
        -200: success or empty pass
        -500: exceptions
    """

    # Create form with frontend data
    form = CreateAssignmentForm(request.form)
    
    # Pass the choices to it
    form.category.choices = assignment_category_choices
    
    # Request course ID
    course_id = int(request.form.get("course_id"))

    # If not passed
    if not course_id:
        return jsonify({
            "success": False,
            "message": "Course ID could not be determined to create the assignment"
        }), 404

    # If form fails validation
    if not form.validate_on_submit():
        return jsonify({
            "success": False,
            "message": f"Form validation Failed. Error: {str(form.errors)}"
        }), 404
    
    try:

        # Fetch session ID
        session_id = find_session_by_number(
            course_id=course_id,
            session_number=int(form.session.data)
        )

        # Create new assignment
        new_assignment = Assignment(
            teacher_id=current_user.id,
            course_id=course_id,
            session_id=session_id,
            pending_stamp=datetime.now(),
            category=form.category.data.lower(),
            description=form.description.data.lower(),
            start_date=form.start_date.data,
            end_date=form.end_date.data
        )
        # Add to db
        db.session.add(new_assignment)
        
        # Flush so that we can use its info
        db.session.flush()

        # Link assignment to student
        check = add_to_assignment(
            assignment_id=new_assignment.id
        )
        
        # If successful
        if check == "success":
            return jsonify({
                "success": True,
                "message": "Successfully sent the assignment to your students"
                }), 200
        
        # If failed
        elif check == "failed":
            return jsonify({
                "success": False,
                "message": "Failed to sent out the assignment"
                }), 404
        
        # If there no students to link to
        elif check == "no_students":
            return jsonify({
                "success": False,
                "message": "No students in this course"
                }), 404
        
        # If there no courses found for the assignment
        elif check == "no_course":
            return jsonify({
                "success": False,
                "message": "No course was found for this assignment"
                }), 404
        
        # Return success
        return jsonify({
            "success": True,
            "message": "Assignment created successfully"
            }), 200
    
    # If exception happens
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error creating assignment: {str(e)}"
            }), 500


@assignment_bp.route("/submit_assignment", methods=["POST"])
@login_required
@student_required
@db_transaction
def submit_assignment():
    """
    Description:
        Submit student assignment and email the file they provide to
    
    Request Parameter:
        -form
        -assignment_id (int)
        -user_type (str)
        -user_id (int)

    Response:
        404: Not available
        200: successful
        500: exception
    """

    # Populate form with frontend data
    form = SubmitAssignmentForm(CombinedMultiDict([request.form, request.files]))

    # Request assignment_id
    assignment_id = int(request.form.get("assignment_id"))

    # Fetch assignment
    assignment , success= find_user_assignments(
        user_type=current_user.role,
        user_id=current_user.id,
        assignment_id=assignment_id
    )

    # If none found
    if not success:
        return jsonify({
            "success": False,
            "message": "Assignment was not found"
            }), 404
    
    # Grab the assignment object from list
    assignment = assignment[0]

    # Fetch teacher of this student
    teacher = find_students_teacher(student_id=current_user.id)

    # If none found
    if teacher == "no_teacher":
        return jsonify({
            "success": False,
            "message": "Teacher was not found"
            }), 404
    
    # If form fails validation
    if not form.validate_on_submit():
        return jsonify({
            "success": False,
            "message": f"Form validation failed. Error: {str(e)}"
        })

    # Store file and note    
    file = form.file.data
    note = form.description.data

    # Email file and note to teacher
    result = email_assignment(
        student=current_user.first_name,
        teacher=teacher,
        file=file,
        note=note
    )

    # IF failed emailing
    if result != "success":
        return jsonify({
            "success": False,
            "message": result
            }), 404

    try:

        # Update assignment status to submitted
        update_assignment_status(
            assignment_id=assignment_id,
            current_status="pending"
            )

        assignment.status = "submitted"

        # Return success
        return jsonify({
            "success": True,
            "message": "Successfully updated assignment status"
            }), 200
    
    # IF exception happens
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error submitting assignment: {e}"
            }), 500


@assignment_bp.route("/score_assignment", methods=["POST"])
@login_required
@teacher_required
@db_transaction
def score_assignment():
    """
    Description:
        Fetch and store scores
    
    Request Parameters:
        -form
        -assignment_id(int)
        -student_id(int)
    
    Response:
        -404: not available
        -200: success
        -500: excepetion
    """

    # Populate form with frontend data
    form = ScoreAssignmentForm(request.form)

    # Request assignment_id
    assignment_id = request.form.get("assignment_id", type=int)
    
    # If not passed
    if not assignment_id:
        return jsonify({
            "success": False,
            "message": "Assginment ID could not be determined"
        }), 404
    
    # Request student_id
    student_id = request.form.get("student_id", type=int)

    # If not passed
    if not student_id:
        return jsonify({
            "success": False,
            "message": "student ID could not be determined to submit scores"
        }), 404
    
    # Fetch category of the assignment
    category = find_assignment_category(assignment_id=assignment_id)

    # IF none found
    if category == "no_category":
        return jsonify({
            "success": False,
            "message": "Assignment category could not be determined"
        }), 404
    
    try:
        # Fetch tags for this assignment
        tags, success = find_tag(assignment_id)

        # If none found
        if not success:
            return jsonify({
            "success": False,
            "message": "Tags not found"
        }), 404

        # Find score choices
        system, form.score.choices, success = find_score_choices(assignment_id=assignment_id)

        if not success:
            return jsonify({
            "success": False,
            "message": "Score options not found"
        }), 404

        # Loop and create a new score element for each tag
        tags = [t[1] for t in tags]
        scores= []
        for i, tag in enumerate(tags):
            score_value = form.score.data[i]
            desc_value = form.description.data[i]
            scores.append(score_value)

            new_score = Score(
                student_id=student_id,
                assignment_id=assignment_id,
                tag=tag,
                category=category,
                score=int(score_value),
                description=desc_value
            )

            # Add each score to db
            db.session.add(new_score)

        # Add assignment average to student
        check = add_assignment_score(
            assignment_id=assignment_id,
            student_id=student_id,
            scores=scores
        )

        # If failed to do so
        if check != "success":
            return jsonify({
                "success": False,
                "message": "Assignment average could not be calculated"
            }), 500
        
        # Update assignemnt status
        check = update_assignment_status(
            assignment_id=assignment_id,
            current_status="submitted"
        )

        # If failed to update
        if check != "scored":
            return jsonify({
            "success": False,
            "message": "Assignment status update failed"
        }), 500

        # Return success
        return jsonify({
            "success": True,
            "message": "Scores were successfully submitted"
            }), 200
    
    # If exception happens
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error submitting scores: {str(e)}"
        }), 500

