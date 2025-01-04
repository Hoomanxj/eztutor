"""
app/queries.py

This module holds all query functions for data base interactions.
"""

from statistics import mean
from werkzeug.security import check_password_hash
from sqlalchemy import func, and_, or_, asc
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta, date
from app.models import *
from app.decorators import db_transaction
from app.choices import numeric_score_choices, descriptive_score_choices


# ==========================
# helper functions
# ==========================


def sort_days(day_list, start_date):
    """
    
    Sort day list of the course based on starting date
    
    Args:
        -list: day_list - list of days for a course
        -date: start - the first date of course
    
    Returns:
        - [], False: If arguments are not given or operation fails
        - sorted_list, True: If success
    """
    if not day_list or not start_date:
        return [], False
    start_date_day = start_date.strftime("%A").lower()
    sorted_list = []
    for i, day in enumerate(day_list):
        if day == start_date_day:
            sorted_list = day_list[i:] + day_list[:i]
            break
    if not sorted_list:
        print(f"Start date day '{start_date_day}' not found in day_list.")
        return [], False
    return sorted_list, True


def weekday_dict(sorted_list, weekday_index):
    """
    
    Create a dictionary of the `sorted_list` based on `weekday_index` dictionary
    
    Args:
        -list: sorted_list
        -list: weekday_index - An index list where each weekay is represented by numbers

    Returns 
        -[], False: If arguments are not given or operation fails
        -w_list, True: If success, a list of dictionaries of weekdays for a course coupled with numbers

    """
    if not sorted_list or not weekday_index:
        return [], False
    w_list = []

    for day in sorted_list:
        for item in weekday_index:
            if day in item:
                w_list.append(item)

    return w_list, True


def create_base_list(w_list):
    """
    
    Modify the value of each day/value pair based on the `start_date`
    
    Args:
        -list: w_list

    Returns:
        -[], False: If arguments are not given or operation fails
        -w_list, True: If success, a list where each days value is its relative distance to start_date
    """
    if not w_list:
        return [], False
    
    # store first session's value for relative computation and set its value to zero
    key, value = next(iter(w_list[0].items()))
    base_value = int(w_list[0][key])
    w_list[0][key] = 0
    # loop through and find the relative distance of each day to start session
    for i, pair in enumerate(w_list[1:]):
        key, value = next(iter(pair.items()))

        if value < base_value:
            pair[key] = 7 - (base_value - value)
        else:
            pair[key] = value - base_value
    return w_list, True


def quotient_remainder(w_list, number_of_session):
    """
    Calculate the number of whole week and remaining days based on `number_of_session`
    
    Args:
        -list: w_list
        -int: number_of_session

    Returns:
        - 0, 0, False: If arguments are not given or operation fails
        - q, r, True: If success, quotient and remainder of number of sessions to week (7 days) division
    """

    if not w_list or not number_of_session:
        return 0, 0, False
    
    weekday_len = len(w_list)
    q = number_of_session // weekday_len
    r = number_of_session % weekday_len
    return q, r, True


def get_timedelta(w_list, q, r):
    """
    
    find `timedelta` values of each session
    
    Args:
        -list: w_list
        -int: q - quotient
        -int: r - remainder
    
    Returns:
        - [], False: If arguments are not given or operation fails
        -deltas, True, If success, a list of deltas to be added to every session to calculate their date
            relative to start date
    """

    if not w_list or not q:
        return [], False
    # calculate timedelta list which finds each session's position in calendar relative to the first session
    deltas = []
    for i in range(q):
        for pair in w_list:
            key, value = next(iter(pair.items()))
            delta = 7*i + pair[key]
            deltas.append(delta)
    for pair in w_list[:r]:
        key, value = next(iter(pair.items()))
        delta = 7 * q + pair[key]
        deltas.append(delta)
    return deltas, True


# ==========================
# find queries
# ==========================


def find_user_courses(user_type=None, user_id=None, course_id=None, course_status=None, assignment_id=None, weekdays=False):
    """
    
    Fetch courses based on different factors.
    
    Args:
        -str: user_type
        -int: user_id
        -int: course_id
        -str: course_status
        -int: assignment_id
        -Bool: weekdays
    
    Returns:
        - [], False: If arguments are not given or operation fails
        - courses, True: if success, a list of dictonaries of course information
    """

    if assignment_id != None: 
        assignment = db.session.query(Assignment).filter(Assignment.id == assignment_id).first()
        course = db.session.query(Course).filter(Course.id == assignment.course_id).all()
        if not course:
            return [], False
        return course, True
    
    elif assignment_id == None:
        if user_type == "teacher":
            # Teacher courses
            query = db.session.query(Course).filter(Course.teacher_id == user_id)
        
        elif user_type == "student":
            # Student courses using the relationship
            query = db.session.query(Course).join(Course.students).filter(Student.id == user_id)

        else:
            return [], False

        if course_id:
            query = query.filter(Course.id == course_id)
        
        if course_status:
            query = query.filter(Course.status == course_status)
        
        user_courses = query.all()
        courses = [{
            "id": c.id,
            "name": c.name,
            "type": c.type,
            "format": c.format,
            "start_hour": c.start_hour.strftime('%H:%M'),
            "status": c.status,
            "code": c.code,
            "weekdays": []
        }for c in user_courses]
        
        if weekdays == True:

            for course in courses: 
                course_weekdays = db.session.query(CourseWeekday).filter(CourseWeekday.course_id == course["id"]).all()
                course_weekdays = [d.name for d in course_weekdays]
                course["weekdays"] = [day for day in course_weekdays]
            return courses, True
        return courses, True


def find_user_assignments(user_type, user_id, course_id=None, assignment_id=None, assignment_status=None):
    """ 
    
    Fetch assignments of a user.
    
    Args:
        -str: user_type
        -int: user_id
        -int: course_id
        -str: course_status
        -int: assignment_id
        -str: assignment_status

    Returns:
        -[], False: If arguments are not given or operation fails
        -user_assignments, True: If success, A list of assignment objects
    """

    if user_type == 'teacher':
        # Teacher assignments
        query = db.session.query(Assignment).filter(Assignment.teacher_id == user_id)
    elif user_type == 'student':
        # Student assignments using the relationship
        query = db.session.query(Assignment).join(Assignment.students).filter(Student.id == user_id)
    else:
        return [], False
    
    if course_id:
        query = query.filter(Assignment.course_id == course_id)
    
    if assignment_id:
        query = query.filter(Assignment.id == assignment_id)
    
    if assignment_status:
        query = query.filter(Assignment.status == assignment_status)

    user_assignments = query.all()

    return user_assignments, True


def email_pass_check(user_type, user_email, user_password):
    """
    
    Check user's email and password
    
    Args:
        -str: user_type
        -str: user_email
        -str: user_password

    Returns:
        -"Unknown user type", False
        -"Wrong email address", False
        -user, True: If success, returns user object
    """

    if user_type == 'teacher':
        user_type = Teacher
    elif user_type == 'student':
        user_type = Student
    else:
        return "Unknown user type", False

    user = db.session.query(user_type).filter(user_type.email == user_email).first()  
    if not user:
        return "Wrong email address", False
    else:
        password_check = check_password_hash(user.password_hash,
                                             user_password)
        if not password_check:
            return "Wrong password", False
        else:
            return user, True


def find_tag(assignment_id):
    """
    Find available tags for a category.

    Args:
        -int: assignment_id

    Returns:
        - [], False: If argument is not passed or query fails
        - tags, True: If success, returns a list of tags    
    """

    category = db.session.query(Assignment).filter(Assignment.id == assignment_id).first().category
    tags = db.session.query(TagCategory).filter(TagCategory.category == category).all()

    if not tags:
        return [], False
    # Produce a tuple to be passed as choices in forms
    tags = [(tag.tag, tag.tag) for tag in tags]
    return tags, True


def find_session(course_id=None, session_id=None, user_type=None, user_id=None, today=None):
    """
    Find sessions based on different factors
    
    Args:
        -int: course_id
        -int: sesison_id
        -str: user_type
        -int: user_id
        -date: today

    Returns:
        [], False: If arguments are not passed or query fails
        [], [], False: If query for session fails
        session, course, True: If success, session and its course dictonaries
    """

    if course_id:
        sessions = db.session.query(Session).filter(Session.course_id == course_id).all()
        if not sessions:
            return [], False
        session_dict = []
        for session in sessions:
            row = {
                "id": session.id,
                "number": session.number,
                "type": session.type,
                "status": session.status,
                "date": session.date.strftime('%Y-%m-%d'), # So that default date would be rendered correctly
                "day": session.day,
                "duration": session.duration,
                "description": session.description
            } 
            session_dict.append(row)
        return session_dict, True
    
    if session_id:
        session = db.session.query(Session).filter(Session.id == session_id).all()
        if not session:
            return [], False
        return session, True
    if today:
        event_filter = or_(
            Session.date > today,
            and_(Session.date == today, Session.start_hour > datetime.now().time())
        )
        if user_type == "teacher":
            session = (db.session.query(Session)
                       .filter(Session.teacher_id == user_id)
                       .filter(event_filter)
                       .order_by(asc(Session.date), asc(Session.start_hour))
                    ).first()
        
        elif user_type == "student":
            session = (db.session.query(Session)
                        .join(Session.students)
                        .filter(Student.id == user_id)
                        .filter(event_filter)
                       .order_by(asc(Session.date), asc(Session.start_hour))
                    ).first()
        if not session:
                return [], [], False
        course = session.course

        return session, course, True


def find_students_teacher(student_id):
    """
    
    Find a teacher by their student's id
    
    Args:
        -int: student_id
    
    Returns:
        -"no_teacher"
        -teacher: If success, returns teacher object
    """
    
    teacher = db.session.query(Teacher).join(Teacher.students).filter(Student.id == student_id).first()
    if not teacher:
        return "no_teacher"
    return teacher


def find_score_choices(course_id=None, assignment_id=None):
    """
    Find score choices
    
    Args:
        -int: course_id
        -int: assignment_id
    
    Returns:
        -[], False: If no system found
        -"numeric", score_choices, True: If success, score choices as list
        -"descriptive", score_choices, True: If success, score choices as list
        -False, [], False: If system is something else
    """
    if assignment_id:
        course_id = db.session.query(Assignment).filter(Assignment.id == assignment_id).first().course_id
        system = db.session.query(Course).filter(Course.id == course_id).first().system
        
    elif course_id:
        system = db.session.query(Course).filter(Course.id == course_id).first().system

        if not system:
            return [], False
        
    if system == "numeric":
        score_choices = numeric_score_choices
        return "numeric", score_choices, True

    elif system == "descriptive":
        score_choices = descriptive_score_choices
        return "descriptive", score_choices, True
    else:
        return False, [], False


def find_schedule(user_type, user_id):
    """
    
    Find user's custom-made schedules
    
    Args:
        -str: user_type
        -int: user_id
    
    Returns:
        -[], False: If arguments are not passed or query fails
        -schedule, True: If success, returns a list of schedule dictionaries
    """

    if user_type == "teacher":
        query = db.session.query(Teacher).filter(Teacher.id == user_id).first()
        schedule_list = query.customtasks
            
    elif user_type == "student":
        query = db.session.query(Student).filter(Student.id == user_id).first()
        schedule_list = query.customtasks
    else:
        return [], False
    
    if not schedule_list:
        return [], False
    
    schedule = [{
            "id": s.id,
            "task": s.task,
            "date": s.date.strftime('%Y-%m-%d'),
            "time_from": s.time_from.strftime('%H:%M'),
            "time_to": s.time_to.strftime('%H:%M')
        } for s in schedule_list]

    
    return schedule, True


def find_class_schedule(user_type, user_id):
    """
    
    Find user's class schedules
    
    Args:
        -str: user_type
        -int: user_id

    Returns:
        -[], False: If arguments are not passed or query fails
        -schedule, True: If success, returns a list of schedule dictionaries
    """

    if user_type == "teacher":
        query = db.session.query(Session).filter(Session.teacher_id == user_id).all()
            
    elif user_type == "student":
        query = db.session.query(Session).join(Session.students).filter(Student.id == user_id).all()

    else:
        return [], False
    
    if not query:
        return [], False

    # Fetch course name (query[0]: since query is a list of objects)
    course_query = db.session.query(Course).filter(Course.id == query[0].course_id).first()
    if not course_query:
        return [], False

    schedule = [{
                "id": s.id,
                "number": s.number,
                "type": s.type,
                "status": s.status,
                "date": s.date.strftime('%Y-%m-%d'), # So that default date would be rendered correctly
                "day": s.day,
                "duration": s.duration,
                "course_name": course_query.name # Adding the same course name to all dictionaries
            }  for s in query]

    
    return schedule, True


def find_all_schedule(user_type, user_id, today=None):
    """
    
    Find user's custom-made and class schedules
    
    Args:
        -str: user_type
        -int: user_id
        -date: today
    
    Returns:
        -[], False: If arguments are not passed or query fails
        -sorted_schedule, True: If success, returns a sorted list of schedule dictionaries
    """
    
    # Ensure 'today' is a string in 'YYYY-MM-DD' format
    if isinstance(today, (date, datetime)):
        today = today.strftime('%Y-%m-%d')
    elif isinstance(today, str):
        today = today.strip()  # Remove any leading/trailing whitespace
    else:
        today = None

    try:
        schedule = []

        if user_type == "teacher":
            # Fetch teacher's custom tasks
            teacher = db.session.query(Teacher).filter(Teacher.id == user_id).first()
            if teacher:
                task_sch = teacher.customtasks
            else:
                task_sch = []

            # Fetch teacher's class schedules
            class_sch_query = db.session.query(Session).filter(Session.teacher_id == user_id).all()

        elif user_type == "student":
            # Fetch student's custom tasks
            student = db.session.query(Student).filter(Student.id == user_id).first()
            if student:
                task_sch = student.customtasks
            else:
                task_sch = []

            # Fetch student's class schedules
            class_sch_query = db.session.query(Session).join(Session.students).filter(Student.id == user_id).all()

        else:
            return [], False

        # Process class schedules
        class_sch = []
        if class_sch_query:
            for session in class_sch_query:
                course = db.session.query(Course).filter(Course.id == session.course_id).first()
                if not course:
                    continue  # Skip if course not found
                class_sch.append({
                    "id": session.id,
                    "type": "class",
                    "name": course.name,
                    "date": session.date.strftime('%Y-%m-%d'),
                    "time_from": session.start_hour.strftime('%H:%M') if session.start_hour else '00:00',
                    "time_to": (datetime.combine(datetime.today(), session.start_hour) + timedelta(minutes=session.duration)).time().strftime('%H:%M') if session.start_hour else '00:00'
                })

        # Process custom tasks
        custom_sch = []
        if task_sch:
            for task in task_sch:
                custom_sch.append({
                    "id": task.id,
                    "type": "custom",
                    "name": task.task,
                    "date": task.date.strftime('%Y-%m-%d'),
                    "time_from": task.time_from.strftime('%H:%M') if task.time_from else '00:00',
                    "time_to": task.time_to.strftime('%H:%M') if task.time_to else '00:00'
                })

        # Combine class schedules and custom tasks
        schedule = class_sch + custom_sch

        # If no schedules are found, return empty list
        if not schedule:
            return [], False

        # Sort the combined schedule by date and start time
        sorted_schedule = sorted(schedule, key=lambda x: (x["date"], x["time_from"]))

        # If a specific date is requested, filter the schedule
        if today:
            sorted_schedule = [s for s in sorted_schedule if s["date"] == today]

        return sorted_schedule, True

    except Exception as e:
        return [], False


def find_student_score(course_id, student_id):
    """
    
    Fetch student scores in a course both for categories and tags
    
    Args:
        -int: course_id
        -int: student_id
    
    Returns:
        -{}, False: If arguments are not passed or query fails
        -scores, True: If success, a dictonary score dictionaries
    """

    try:
        # Scores aggregated by category
        cat_query = (
            db.session.query(AssignmentStudent.category, func.avg(AssignmentStudent.score))
            .join(Assignment, AssignmentStudent.assignment_id == Assignment.id)  # Explicit join
            .filter(AssignmentStudent.score != None)
            .filter(AssignmentStudent.student_id == student_id)
            .filter(Assignment.course_id == course_id)
            .group_by(AssignmentStudent.category)  # or Assignment.category, depending on your logic
        ).all()

        cat_scores = {category: round(avg or 0, 2) for category, avg in cat_query}

        # Scores aggregated by category and tag
        tag_query = (
            db.session.query(Score.category, Score.tag, func.avg(Score.score))
            .join(Assignment, Score.assignment_id == Assignment.id)
            .filter(Score.student_id == student_id)
            .filter(Assignment.course_id == course_id)
            .group_by(Score.category, Score.tag)
        ).all()  # Execute the query

        # Grouping tag scores by category
        tag_scores_by_category = {}
        for category, tag, avg in tag_query:
            if category not in tag_scores_by_category:
                tag_scores_by_category[category] = {}
            tag_scores_by_category[category][tag] = round(avg or 0, 2)

        # Filtering tag scores by category
        categories = ["speaking", "listening", "writing", "reading"]
        tag_scores = {}
        for category in categories:
            tag_scores[category] = tag_scores_by_category.get(category, {})

        scores = {"cat_scores": cat_scores, "tag_scores": tag_scores}

        return scores, True

    except Exception as e:
        return {}, False


def unique_email_check(user_type, email):
    """
    Check whether this email is already registered or not
    
    Args:
        -str: user_type
        -str: email
    
    Returns:
        -False: If query fails
        -True: If success
    """

    if user_type == "teacher":
        model = Teacher
    elif user_type == "student":
        model = Student

    check = db.session.query(model).filter(model.email == email).first()
    
    if not check:
        return True
    return False


def find_students(course_id):
    """
    Fetch students
    
    Args:
        -int: course_id
    
    Returns:
        -[], False: If query fails
        -students, True: A list of student dictonaries
    """

    students = db.session.query(Student).join(Student.courses).filter(Course.id == course_id).all()

    if not students:
        return [], False
    
    students = [{
        "id": s.id,
        "name": s.first_name + ' ' + s.last_name,
    } for s in students]

    return students, True


def find_assignment_category(assignment_id):
    """
    Fetch category of a given assignment
    
    Args:
        -int: assignment_id
    
    Returns:
        -"no_category"
        -category: If success, category type as str
    """

    category = db.session.query(Assignment).filter(Assignment.id == assignment_id).first().category
    if not category:
        return "no_category"
    return category


def find_session_by_number(course_id, session_number):
    """
    Find sessions by their session number
    
    Args:
        -int: course_id
        -int: session_number
    
    Returns:
        -"no_id"
        -session_id: If success
    """
        
    session_id = (
        db.session.query(Session)
        .filter(Session.course_id == course_id)
        .filter(Session.number == session_number)
        ).first().id
    if not session_id:
        return "no_id"
    return session_id


# ==========================
# update queries
# ==========================


def update_assignment_status(assignment_id, current_status):
    """
    Update the status of an assignment and
        timestamping the relevant stamp column
    
    Args:
        -int: assignment_id
        -str: current_status
    
    Returns:
        -error
        -assignment.status: If success
    """
    
    try:
        assignment = db.session.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            return "No assignment was found"
        assignment.status = current_status

        if current_status == "pending":
            assignment.status = "submitted"
            assignment.submitted_stamp = datetime.now()
        
        elif current_status == "submitted":
            assignment.status = "scored"
            assignment.scored_stamp = datetime.now()

        db.session.commit()
        return assignment.status
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Error: {e}"


def update_session(session_id, session_type=None, session_status=None, session_date=None,
                   session_day=None, session_duration=None, session_description=None):
    """
    Update session information
    
    Args:
        -int: session_id
        -str: session_type
        -str: session_status
        -date: session_date
        -str: session_day
        -int: session_duration
        -str: session_description
    
    Returns:
        -"no_session"
        -"success"
        -error
    """

    session = db.session.query(Session).filter(Session.id == session_id).first()
    if not session:
        return "no_session", False

    try:
        if session_type is not None:
            session.type = session_type
        if session_status is not None:
            session.status = session_status
        if session_date is not None:
            session.date = session_date
        if session_day is not None:
            session.day = session_day
        if session_duration is not None:
            session.duration = session_duration
        if session_description is not None:
            session.description = session_description

        db.session.commit()
        return "success", True
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Error: {str(e)}", False


def add_student(student_id, course_code):
    """
    
    Add a student to a course using course code
    
    Args:
        -int: student_id
        -str: course_code
    
    Returns
        -course.name, "enrolled": If user is already enrolled
        -course.name, "succcess"
        -course.name, "failed"
    """

    # Fetch the course
    course = db.session.query(Course).filter(Course.code == course_code).first()
    try:
        # Check if they already are in the course
        check = (db.session.query(CourseStudent)
                .filter(CourseStudent.course_id == course.id)
                .filter(CourseStudent.student_id == student_id)
                ).all()
        if check:
            return course.name, "enrolled"
        
        # Check if student is already linked to this teacher
        check = (db.session.query(TeacherStudent)
                .filter(TeacherStudent.student_id == student_id)
                .filter(TeacherStudent.teacher_id == course.teacher_id) 
                ).first()
        # Link student to teacher if they are not already
        if not check:
            new_entry = TeacherStudent(
                teacher_id = course.teacher_id,
                student_id = student_id
            )
            db.session.add(new_entry)

        # Link student to Course table via CourseStudent table
        add_to_course = CourseStudent(
            course_id = course.id,
            student_id = student_id
        )
        db.session.add(add_to_course)
        
        # Fetch relevant sessions
        sessions = db.session.query(Session).filter(Session.course_id == course.id).all()
        # Link the student to Session table via SessionStudent table
        session_ids = [s.id for s in sessions]
        for id in session_ids:
            add_to_session = SessionStudent(
                session_id=id,
                student_id=student_id
            )
            db.session.add(add_to_session)
        # Commit if all entries succeed
        db.session.commit()

        print("student was successfully added to course")
        return course.name, "success"
    
    except Exception as e:
        # Rollback if any entry fails
        db.session.rollback()
        print("Failed to add the student to the course", e)
        return course.name, "failed"


def add_to_assignment(assignment_id):
    """
    
    Add a student to an assignment
    
    Args:
        -int: assignment_id
    
    Returns:
        -"no_course"
        -"no_students"
        -"success"
        -"failed"
    """

    try:
        assignment = db.session.query(Assignment).filter(Assignment.id == assignment_id).first()
        course = db.session.query(Course).filter(Course.id == assignment.course_id).first()
        if not course:
            return "no_course"
        students = course.students
        if not students:
            return "no_students"
        student_ids = [student.id for student in students]

        # Link student to Assignment table via AssignmentStudent table
        for id in student_ids:
            new_entry = AssignmentStudent(
                assignment_id = assignment_id,
                student_id = id,
                category = assignment.category
            )
            db.session.add(new_entry)
        
        db.session.commit()

        return "success"
    
    except Exception as e:
        db.session.rollback()
        print("Failed to add the student to the assignment", e)
        return "failed"


def add_assignment_score(assignment_id,student_id , scores):
    """
    
    Calculate assignment score based on tag scores
    
    Args:
        int: assignment_id
        int: student_id
        list: scores
    
    Returns:
        -"no_assignment"
        -"success"
        -error
    """

    assignment = (
        db.session.query(AssignmentStudent)
        .filter(AssignmentStudent.assignment_id == assignment_id)
        .filter(AssignmentStudent.student_id == student_id)
        ).first()
    if not assignment:
        return "no_assignment"
    try:
        assignment.score = round(mean(scores))
        db.session.commit()
        return "success"
    except Exception as e:
        db.session.rollback()
        return str(e)


# ==========================
# populate queries
# ==========================


@db_transaction
def populate_sessions(user_id, course_id, start_date, start_hour, number_of_session, day_list, duration):
    """
    
    Populate the sessions for a course when it is created
    
    Args:
        -int: user_id
        -int: course_id
        -date: start_date
        -time: start_hour
        -int: number_of_session
        -list: day_list
        -int: duration
    
    Returns:
        - ValueError: If fails at any stage
    """
    try:        
        weekday_index = [
            {"monday": 1}, {"tuesday": 2}, {"wednesday": 3},
            {"thursday": 4}, {"friday": 5}, {"saturday": 6}, {"sunday": 7},
        ]
        
        sorted_list, success = sort_days(day_list=day_list, start_date=start_date)
        if not success:
            raise ValueError("Problem in sorting days")
        
        w_list, success = weekday_dict(sorted_list, weekday_index)
        if not success:
            raise ValueError("Problem in getting w_list")
        
        w_list, success = create_base_list(w_list=w_list)
        if not success:
            raise ValueError("Problem in getting base w_list")
        
        q, r, success = quotient_remainder(w_list=w_list, number_of_session=number_of_session)
        if not success:
            raise ValueError("Problem in getting q and r")
        
        deltas, success = get_timedelta(w_list=w_list, q=q, r=r)
        if not success:
            raise ValueError("Problem in getting deltas")
        
        for i in range(number_of_session):
            if i >= len(deltas):
                break
            session_date = start_date + timedelta(days=deltas[i])
            new_session = Session(
                teacher_id=user_id,
                course_id=course_id,
                number=i + 1,
                type="normal",
                status="pending",
                date=session_date,
                start_hour=start_hour,
                day=session_date.strftime("%A").lower(),
                duration=duration
            )
            db.session.add(new_session)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise


