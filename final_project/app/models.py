# pylint: disable=C0115, R0903

"""
This module contains the SQLAlchemy models for the application,
including the definition of tables and relationships.
"""
from sqlalchemy import CheckConstraint
from app import db


gender_choice = ["male", "female", "none-binary"]
education_level = ["college", "bachelor's", "master's", "doctoral"]
category = ["speaking", "listening", "writing", "reading"]
session_type = ["normal", "makeup"]
course_type = ["online", "on-site"]
course_format = ["private", "group"]
session_status = ["pending", "canceled", "held"]
week_day = ["monday", "tuesday", "wednesday", "thursday", "friday",
            "saturday", "sunday"
            ]
attendance_status = ["present", "absent"]
assignment_status = ["deliverd", "pending"]
tags = [
    "lexical resources",
    "grammatical range",
    "task achievement",
    "coherence",
    "cohesion",
    "pronunciation",
    "fluency",
    "comprehension",
]


class Teacher(db.Model):
    """
    a table to store teacher' personal information
    """

    __tablename__ = "teacher"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum(*gender_choice))
    zeus = db.Column(db.String(100), nullable=False)
    cell = db.Column(db.String(60))
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    address = db.Column(db.Text)
    education_level = db.Column(db.Enum(*education_level), nullable=False)
    field_of_study = db.Column(db.String(200), nullable=False)
    native_language = db.Column(db.String(50), nullable=False)
    teaching_language = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Teacher {self.name}>'


class Student(db.Model):
    """
    a table to store student' personal information
    """

    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'),
                           nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum(*gender_choice))
    zeus = db.Column(db.String(100), nullable=False)
    cell = db.Column(db.String(60))
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    address = db.Column(db.Text)
    education_level = db.Column(db.Enum(*education_level), nullable=False)
    field_of_study = db.Column(db.String(200), nullable=False)
    native_language = db.Column(db.String(50), nullable=False)
    learning_language = db.Column(db.String(50), nullable=False)
    teacher = db.relationship('Teacher', backref='student')

    def __repr__(self):
        return f'<Student {self.name}>'


class Course(db.Model):
    """
    a table to store course information
    """

    __tablename__ = "course"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'),
                           nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
                           nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(*course_type), nullable=False)
    format = db.Column(db.Enum(*course_format), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    number_of_session = db.Column(db.Integer)
    session_duration = db.Column(db.SmallInteger, nullable=False)
    number_of_student = db.Column(db.SmallInteger, nullable=False)
    teacher = db.relationship('Teacher', backref='course')
    student = db.relationship('Student', backref='course')


    def __repr__(self):
        return f'<Course {self.name}>'


class CourseWeekday(db.Model):
    """
    a table to store days of the week for each course
    """

    __tablename__ = "courseweekday"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'),
                          nullable=False)
    name = db.Column(db.Enum(*week_day), nullable=False)
    course = db.relationship('Course', backref='weekday')

    def __repr__(self):
        return f'<CourseWeekday {self.name}>'


class Session(db.Model):
    """
    a table to store session information
    """

    __tablename__ = "session"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'),
                           nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
                           nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'),
                          nullable=False)
    type = db.Column(db.Enum(*session_type), nullable=False)
    status = db.Column(db.Enum(*session_status), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.SmallInteger, nullable=False)
    description = db.Column(db.Text, nullable=False)
    teacher = db.relationship('Teacher', backref='session')
    student = db.relationship('Student', backref='session')
    course = db.relationship('Course', backref='session')

    def __repr__(self):
        return f'<Session {self.id}>'


class Attendance(db.Model):
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


class Assignment(db.Model):
    """
    a table to store assignment information
    """

    __tablename__ = "assignment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'),
                           nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
                           nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'),
                          nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'),
                           nullable=False)
    status = db.Column(db.Enum(*assignment_status), nullable=False)
    category = db.Column(db.Enum(*category), nullable=False)
    description = db.Column(db.Text, nullable=False)
    score = db.Column(db.Float)
    start_date = db.Column(db.DateTime, nullable=False)
    submission_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    teacher = db.relationship('Teacher', backref='assignment')
    student = db.relationship('Student', backref='assignment')
    course = db.relationship('Course', backref='assignment')
    session = db.relationship('Session', backref='assignment')

    def __repr__(self):
        return f'<Assignment {self.id}>'


class ReportCard(db.Model):
    """
    a table to store ReportCard information
    """

    __tablename__ = "ReportCard"

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
    score = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    teacher = db.relationship('Teacher', backref='ReportCard')
    student = db.relationship('Student', backref='ReportCard')
    session = db.relationship('Session', backref='ReportCard')
    assignment = db.relationship('Assignment', backref='ReportCard')

    __table_args__ = (
        CheckConstraint('score <= 100 AND score >= 0', name='score_range'),
    )

    def __repr__(self):
        return f'<ReportCard {self.id}>'


class Progress(db.Model):
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
    date = db.Column(db.DateTime,)
    teacher = db.relationship('Teacher', backref='progress')
    student = db.relationship('Student', backref='progress')
    course = db.relationship('Course', backref='progress')

    def __repr__(self):
        return f'<Progress {self.id}>'


class Score(db.Model):
    """
    a table to store scores
    """

    __tablename__ = "score"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'),
                              nullable=False)
    tag = db.Column(db.Enum(*tags), nullable=False)
    value = db.Column(db.SmallInteger, nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime)
    
    assignment = db.relationship('Assignment', backref='assingment-score')

    def __repr__(self):
        return f'<Score {self.id}>'


class TeacherLink(db.Model):
    """
    a table to store links to social media accounts, websites and platforms
    """

    __tablename__ = "teacher_link"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    url = db.Column(db.String(512), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'),
                           nullable=False)
    teacher = db.relationship('Teacher', backref='teacher_link')

    def __repr__(self):
        return f'<Teacher_Link {self.teacher_url}>'


class StudentLink(db.Model):
    """
    a table to store links to social media accounts, websites and platforms
    """

    __tablename__ = "student_link"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False)
    url = db.Column(db.String(512), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
                           nullable=False)
    student = db.relationship('Student', backref='student_link')

    def __repr__(self):
        return f'<Student_Link {self.student_url}>'
