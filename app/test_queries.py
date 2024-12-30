"""
app/test_queries.py

This module only used for development purposes.
"""

from datetime import datetime, timedelta, date
from statistics import mean
from werkzeug.security import check_password_hash
from . import create_app
from sqlalchemy import func, and_, or_, asc
from uuid import uuid4
from flask import url_for
from app.extentions import db
from app.models import *
from app.queries import find_tag, find_user_courses
from app.forms import numeric_score_choices, descriptive_score_choices




app = create_app()

def find_all_schedule(user_type, user_id, today=None):
    """ Find user's custom-made and class schedules """
    print("today:", today)
     # Ensure 'today' is a string in 'YYYY-MM-DD' format
    if isinstance(today, (date, datetime)):
        today_str = today.strftime('%Y-%m-%d')
    elif isinstance(today, str):
        today_str = today.strip()  # Remove any leading/trailing whitespace
    else:
        today_str = None
    with app.app_context():
        try:
            schedule = []

            if user_type == "teacher":
                # Fetch teacher's custom tasks
                teacher = db.session.query(Teacher).filter(Teacher.id == user_id).first()
                if teacher:
                    task_sch = teacher.customtasks
                    print("custom task:", task_sch)
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
            print("processed custom schedule:", custom_sch)

            # Combine class schedules and custom tasks
            schedule = class_sch + custom_sch

            # If no schedules are found, return empty list
            if not schedule:
                return [], False

            # Sort the combined schedule by date and start time
            sorted_schedule = sorted(schedule, key=lambda x: (x["date"], x["time_from"]))
            print("sorted schedule:", sorted_schedule)
            # If a specific date is requested, filter the schedule
            if today:
                filtered_schedule = [s for s in sorted_schedule if s["date"] == today_str]
                print("filtered schedule:", filtered_schedule)

            return filtered_schedule, True

        except Exception as e:
            # Log the exception for debugging purposes
            print(f"Error in find_all_schedule: {str(e)}")
            return [], False

check = find_all_schedule(
    user_type="teacher",
    user_id=6,
    today=datetime.today().date()
)
print("result:", check)


def find_all_schedule(user_type, user_id, today=None):
    """ Find user's custom-made schedules """

    with app.app_context():
        if user_type == "teacher":

            # Fetch task schedule
            task_sch = db.session.query(Teacher).filter(Teacher.id == user_id).first().customtasks

            # Fetch class schedule
            query = db.session.query(Session).filter(Session.teacher_id == user_id).all()
                
        elif user_type == "student":

            # Fetch task schedule
            task_sch = db.session.query(Student).filter(Student.id == user_id).first().customtasks

            # Fetch class schedule
            query = db.session.query(Session).join(Session.students).filter(Student.id == user_id).all()

        else:
            return [], False
        
        if not task_sch:
            return [], False
        
        # Fetch course name (query[0]: since query is a list of objects)
        course_query = db.session.query(Course).filter(Course.id == query[0].course_id).first()
        if not course_query:
            return [], False

        class_sch = [{
                    "id": s.id,
                    "type": "class",
                    "name": course_query.name, # Adding the same course name to all dictionaries
                    "date": s.date.strftime('%Y-%m-%d'), # So that default date would be rendered correctly
                    "time_from": s.start_hour.strftime('%H:%M') if s.start_hour else '00:00',
                    # Using duration to find class end time
                    "time_to": (datetime.combine(datetime.today(), s.start_hour) + timedelta(minutes=s.duration)).time().strftime('%H:%M') if s.start_hour else '00:00'
                }  for s in query]

        task_sch = [{
                "id": s.id,
                "type": "custom",
                "name": s.task,
                "date": s.date.strftime("%Y-%m-%d"),
                "time_from": s.time_from.strftime('%H:%M') if s.time_from else '00:00',
                "time_to": s.time_to.strftime('%H:%M') if s.time_from else '00:00'
            } for s in task_sch]

        schedule = class_sch + task_sch

        sorted_schedule = sorted(schedule, key=lambda x: (x["date"], x["time_from"]))
        if today:
            sorted_schedule = [s for s in sorted_schedule if s["date"] == today]
        
        return sorted_schedule, True
