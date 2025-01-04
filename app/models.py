"""
app/models.py

This module contains the SQLAlchemy models for the application,
including the definition of tables and relationships.
"""
from datetime import datetime
from sqlalchemy import func
from flask_login import UserMixin
from app.extentions import db




gender_choice = ["male", "female", "other"]
education_level = ["high school or less", "college", "bachelor's", "master's", "doctoral"]
category = ["speaking", "listening", "writing", "reading"]
session_type = ["normal", "makeup"]
session_status = ["pending", "cancelled", "held"]
course_type = ["online", "on-site"]
course_format = ["private", "group"]
course_status = ["ongoing", "concluded"]
week_day = ["monday", "tuesday", "wednesday", "thursday", "friday",
            "saturday", "sunday"
            ]
attendance_status = ["present", "absent"]
assignment_status = ["pending", "submitted", "scored"]
tags = [
    "lexical resources", "grammatical range", "task achievement",
    "coherence", "cohesion", "pronunciation", "fluency", "comprehension",
]
grading_system = [
    "numeric", "descriptive"  
]


grading_scores = [
    {"value": 0, "label": "No Attempt"},
    {"value": 1, "label": "Failing"},
    {"value": 2, "label": "Very Poor"},
    {"value": 3, "label": "Poor"},
    {"value": 4, "label": "Weak Pass"},
    {"value": 5, "label": "Mediocre"},
    {"value": 6, "label": "Satisfactory"},
    {"value": 7, "label": "Above Average"},
    {"value": 8, "label": "Good"},
    {"value": 9, "label": "Very Good"},
    {"value": 10, "label": "Excellent"},
]

class TimestampMixin:
    """ A simple class to add timestamp to each table """
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)


class Teacher(db.Model, UserMixin, TimestampMixin):
    """
    a table to store teacher' personal information
    """

    __tablename__ = "teacher"
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True,
                   nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum(*gender_choice), nullable=True)
    email = db.Column(db.String(100), unique=True,
                      nullable=False)
    cell = db.Column(db.String(60), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)
    education_level = db.Column(db.Enum(*education_level),
                                nullable=False)
    field_of_study = db.Column(db.String(200), nullable=False)
    native_language = db.Column(db.String(50), nullable=False)
    teaching_language = db.Column(db.String(50),
                                  nullable=False)
    password_hash = db.Column(db.Text, nullable=True)
    role = db.Column(db.String(20), default='teacher',
                     nullable=False)

    students = db.relationship('Student', secondary='teacherstudent',
                               back_populates='teachers')
    courses = db.relationship('Course', back_populates='teacher')
    sessions = db.relationship('Session', back_populates='teacher')
    assignments = db.relationship('Assignment', back_populates='teacher')
    links = db.relationship('TeacherLink', back_populates='teacher')
    customtasks = db.relationship('CustomTask', back_populates='teacher')

    def get_id(self):
        return str(self.id)


class Student(db.Model, UserMixin, TimestampMixin):
    """
    a table to store student' personal information
    """

    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum(*gender_choice),
                       nullable=True)
    email = db.Column(db.String(100), unique=True,
                      nullable=False)
    cell = db.Column(db.String(60), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)
    education_level = db.Column(db.Enum(*education_level),
                                nullable=False)
    field_of_study = db.Column(db.String(200), nullable=False)
    native_language = db.Column(db.String(50), nullable=False)
    learning_language = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.Text, nullable=True)
    role = db.Column(db.String(20), default='student',
                     nullable=False)

    teachers = db.relationship('Teacher', secondary='teacherstudent',
                               back_populates='students')
    courses = db.relationship('Course', secondary='coursestudent',
                              back_populates='students')
    assignments = db.relationship('Assignment', secondary='assignmentstudent',
                                  back_populates='students')
    sessions = db.relationship('Session', secondary='sessionstudent',
                               back_populates='students')
    scores = db.relationship('Score', back_populates='student')
    links = db.relationship('StudentLink', back_populates='student')
    customtasks = db.relationship('CustomTask', back_populates='student')
    

    def get_id(self):
        return str(self.id)


class TeacherStudent(db.Model, TimestampMixin):
    """ Link teachers to students """
    
    __tablename__ = "teacherstudent"

    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'),
                           primary_key=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
                           primary_key=True, nullable=False)
    

class Course(db.Model, TimestampMixin):
    """
    a table to store course information
    """

    __tablename__ = "course"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'),
                           nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(*course_type), nullable=False)
    format = db.Column(db.Enum(*course_format), nullable=False)
    system = db.Column(db.Enum(*grading_system), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    start_hour = db.Column(db.Time, nullable=False)
    number_of_session = db.Column(db.Integer, nullable=False)
    session_duration = db.Column(db.Integer, nullable=False)
    number_of_student = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(*course_status), default="ongoing", nullable=False)
    code = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(255), nullable=True)

    teacher = db.relationship('Teacher', back_populates='courses')
    students = db.relationship('Student', secondary='coursestudent',
                               back_populates='courses')
    weekdays = db.relationship('CourseWeekday', back_populates='courses')
    sessions = db.relationship('Session', back_populates='course')
    assignments = db.relationship('Assignment', back_populates='course')


    def __repr__(self):
        return f'<Course {self.name}>'


class CourseWeekday(db.Model, TimestampMixin):
    """
    a table to store days of the week for each course
    """

    __tablename__ = "courseweekday"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'),
                          nullable=False)
    name = db.Column(db.Enum(*week_day), nullable=False)

    courses = db.relationship('Course', back_populates='weekdays')

    def __repr__(self):
        return f'<CourseWeekday {self.name}>'


class CourseStudent(db.Model, TimestampMixin):
    """ a table to connect students ot courses """

    __tablename__ = 'coursestudent'

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'),
                          primary_key=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
                           primary_key=True, nullable=False)


class Session(db.Model, TimestampMixin):
    """
    a table to store session information
    """

    __tablename__ = "session"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'),
                           nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'),
                          nullable=False)
    number = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Enum(*session_type), default="normal",
                     nullable=False)
    status = db.Column(db.Enum(*session_status), default="pending",
                       nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_hour = db.Column(db.Time, nullable=False)
    day = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, default="", nullable=True)

    teacher = db.relationship('Teacher', back_populates='sessions')
    course = db.relationship('Course', back_populates='sessions')
    students = db.relationship('Student', secondary='sessionstudent',
                               back_populates='sessions')
    assignments = db.relationship('Assignment',back_populates='session')

    def __repr__(self):
        return f'<Session {self.id}>'


class SessionStudent(db.Model, TimestampMixin):
    """ a table to connect students ot sessions """

    __tablename__ = 'sessionstudent'

    session_id = db.Column(db.Integer, db.ForeignKey('session.id'),
                          primary_key=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
                           primary_key=True, nullable=False)


class Assignment(db.Model):
    """
    a table to store assignment information
    """

    __tablename__ = "assignment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'),
                           nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'),
                          nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'),
                           nullable=False)
    status = db.Column(db.Enum(*assignment_status), default="pending",
                       nullable=False)
    pending_stamp = db.Column(db.DateTime, nullable=True)
    submitted_stamp = db.Column(db.DateTime, nullable=True)
    scored_stamp = db.Column(db.DateTime, nullable=True)
    category = db.Column(db.Enum(*category), nullable=False)
    description = db.Column(db.Text, nullable=False)
    score = db.Column(db.Float, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    submission_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)

    teacher = db.relationship('Teacher', back_populates='assignments')
    students = db.relationship('Student', secondary='assignmentstudent',
                              back_populates='assignments')
    course = db.relationship('Course', back_populates='assignments')
    session = db.relationship('Session', back_populates='assignments')
    scores = db.relationship('Score', back_populates='assignment')

    def __repr__(self):
        return f'<Assignment {self.id}>'


class AssignmentStudent(db.Model, TimestampMixin):
    """ a table to connect students ot assignments """

    __tablename__ = 'assignmentstudent'

    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'),
                          primary_key=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
                           primary_key=True, nullable=False)
    category = db.Column(db.Enum(*category), nullable=False)
    score = db.Column(db.Integer, nullable=True)


class TagCategory(db.Model, TimestampMixin):
    """ A table to store tags and categorize them """

    __tablename__ = 'tagcategory'

    id = db.Column(db.Integer, primary_key=True,
                   nullable=False)
    tag = db.Column(db.Enum(*tags), nullable=False)
    category = db.Column(db.Enum(*category), nullable=False)
    description = db.Column(db.Text, nullable=False)


class Score(db.Model, TimestampMixin):
    """
    a table to store scores
    """

    __tablename__ = "score"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'),
                              nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
                           nullable=False)
    category = db.Column(db.Enum(*category), nullable=False)
    tag = db.Column(db.Enum(*tags), nullable=False)
    score = db.Column(db.SmallInteger, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    assignment = db.relationship('Assignment', back_populates='scores')
    student = db.relationship('Student', back_populates='scores')

    def __repr__(self):
        return f'<Score {self.id}>'


class CustomTask(db.Model, TimestampMixin):
    """ A table to store user's custom-made tasks for calendar"""
    __tablename__ = "customtask"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'),
                           nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
                           nullable=True)
    task = db.Column(db.String(255), default="", nullable=False)
    date = db.Column(db.Date, nullable=False)
    time_from = db.Column(db.Time, nullable=False)
    time_to = db.Column(db.Time, nullable=False)

    teacher = db.relationship('Teacher', back_populates='customtasks')
    student = db.relationship('Student', back_populates='customtasks')

    def __repr__(self):
        return f'<CustomTask {self.task}>'


##################################################
# Unused tables
##################################################

class Attendance(db.Model, TimestampMixin):
    """
    a table to track student attendance    
    """
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
                           nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'),
                           nullable=False)
    status = db.Column(db.Enum(*attendance_status), nullable=False)

    student = db.relationship('Student', backref='attendance')
    session = db.relationship('Session', backref='attendance')

    def __repr__(self):
        return f'<Attendance {self.status}>'
    

class ReportCard(db.Model, TimestampMixin):
    """
    a table to store ReportCard information
    """

    __tablename__ = "reportcard"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'),
                           nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
                           nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'),
                           nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'),
                              nullable=False)
    score = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)

    teacher = db.relationship('Teacher', backref='reportcard')
    student = db.relationship('Student', backref='reportcard')
    session = db.relationship('Session', backref='reportcard')
    assignment = db.relationship('Assignment', backref='reportcard')

    def __repr__(self):
        return f'<ReportCard {self.id}>'


class Progress(db.Model, TimestampMixin):
    """
    a table to store progress information
    """

    __tablename__ = "progress"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'),
                           nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
                           nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'),
                          nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=True)

    teacher = db.relationship('Teacher', backref='progress')
    student = db.relationship('Student', backref='progress')
    course = db.relationship('Course', backref='progress')

    def __repr__(self):
        return f'<Progress {self.id}>'


class Language(db.Model, TimestampMixin):
    """
    a table to store languages
    """
    
    __tablename__ = 'language'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Language {self.name}>'


class TeacherLink(db.Model, TimestampMixin):
    """
    a table to store links to social media accounts, websites and platforms
    """

    __tablename__ = "teacher_link"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'),
                           nullable=False)
    url = db.Column(db.String(512), nullable=False)

    teacher = db.relationship('Teacher', back_populates='links')

    def __repr__(self):
        return f'<Teacher_Link {self.teacher_url}>'


class StudentLink(db.Model, TimestampMixin):
    """
    a table to store links to social media accounts, websites and platforms
    """

    __tablename__ = "student_link"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
                           nullable=False)
    url = db.Column(db.String(512), nullable=False)

    student = db.relationship('Student', back_populates='links')

    def __repr__(self):
        return f'<Student_Link {self.student_url}>'

