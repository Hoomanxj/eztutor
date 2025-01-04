"""
app/factories.py

This module help populating data base with dummy data and only has developmental value.
"""

import factory
from faker import Faker
from app import db
from app.models import *

durations = [45, 60, 90]
fake = Faker()

# Teacher Factory
class TeacherFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Populate Teacher table with random data for test 
    """
    class Meta:
        model = Teacher
        sqlalchemy_session = db.session

    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    date_of_birth = factory.LazyAttribute(lambda _: fake.date_of_birth(minimum_age=18))
    gender = factory.LazyAttribute(lambda _: fake.random_element(elements=gender_choice))
    email = factory.LazyAttribute(lambda _: fake.email())
    cell = factory.LazyAttribute(lambda _: fake.phone_number())
    country = factory.LazyAttribute(lambda _: fake.country())
    address = factory.LazyAttribute(lambda _: fake.address())
    education_level = factory.LazyAttribute(lambda _: fake.random_element(elements=education_level))
    field_of_study = factory.LazyAttribute(lambda _: fake.job())
    native_language = factory.LazyAttribute(lambda _: fake.language_name())
    teaching_language = factory.LazyAttribute(lambda _: fake.language_name())

# Student Factory
class StudentFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Populate Student table with random data for test 
    """
    class Meta:
        model = Student
        sqlalchemy_session = db.session

    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    date_of_birth = factory.LazyAttribute(lambda _: fake.date_of_birth(minimum_age=10))
    gender = factory.LazyAttribute(lambda _: fake.random_element(elements=gender_choice))
    email = factory.LazyAttribute(lambda _: fake.email())
    cell = factory.LazyAttribute(lambda _: fake.phone_number())
    country = factory.LazyAttribute(lambda _: fake.country())
    address = factory.LazyAttribute(lambda _: fake.address())
    education_level = factory.LazyAttribute(lambda _: fake.random_element(elements=education_level))
    field_of_study = factory.LazyAttribute(lambda _: fake.job())
    native_language = factory.LazyAttribute(lambda _: fake.language_name())
    learning_language = factory.LazyAttribute(lambda _: fake.language_name())

    teacher = factory.SubFactory('app.factories.TeacherFactory')

# Course Factory
class CourseFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Populate Course table with random data for test 
    """
    class Meta:
        model = Course
        sqlalchemy_session = db.session

    name = factory.LazyAttribute(lambda _: fake.word())
    type = factory.LazyAttribute(lambda _: fake.random_element(elements=course_type))
    format = factory.LazyAttribute(lambda _: fake.random_element(elements=course_format))
    description = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=20))
    start_date = factory.LazyAttribute(lambda _: fake.date_this_year())
    end_date = factory.LazyAttribute(lambda obj: fake.date_between(start_date=obj.start_date, end_date='+1d'))
    number_of_session = factory.LazyAttribute(lambda _: fake.random_int(min=10, max=50))
    session_duration = factory.LazyAttribute(lambda _: fake.random_element(elements=durations) or 45)
    number_of_student = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=30))

    teacher = factory.SubFactory('app.factories.TeacherFactory')
    student = factory.SubFactory('app.factories.StudentFactory')

# Session Factory
class SessionFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Populate Session table with random data for test 
    """
    class Meta:
        model = Session
        sqlalchemy_session = db.session

    type = factory.LazyAttribute(lambda _: fake.random_element(elements=session_type))
    status = factory.LazyAttribute(lambda _: fake.random_element(elements=session_status))
    date = factory.LazyAttribute(lambda _: fake.date())
    duration = factory.LazyAttribute(lambda _: fake.random_element(elements=durations) or 45)
    print({duration})
    description = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=50))

    teacher = factory.SubFactory('app.factories.TeacherFactory')
    student = factory.SubFactory('app.factories.StudentFactory')
    course = factory.SubFactory('app.factories.CourseFactory')

# Attendance Factory
class AttendanceFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Populate Attendance table with random data for test 
    """
    class Meta:
        model = Attendance
        sqlalchemy_session = db.session

    status = factory.LazyAttribute(lambda _: fake.random_element(elements=attendance_status))

    student = factory.SubFactory('app.factories.StudentFactory')
    session = factory.SubFactory('app.factories.SessionFactory')

# Assignment Factory
class AssignmentFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Populate Assignment table with random data for test 
    """
    class Meta:
        model = Assignment
        sqlalchemy_session = db.session

    status = factory.LazyAttribute(lambda _: fake.random_element(elements=assignment_status))
    category = factory.LazyAttribute(lambda _: fake.random_element(elements=category))
    description = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=50))
    score = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=100))
    start_date = factory.LazyAttribute(lambda _: fake.date_this_year())
    submission_date = factory.LazyAttribute(lambda obj: fake.date_between(start_date=obj.start_date, end_date='+1d'))
    end_date = factory.LazyAttribute(lambda obj: fake.date_between(start_date=obj.submission_date, end_date='+1d'))

    teacher = factory.SubFactory('app.factories.TeacherFactory')
    student = factory.SubFactory('app.factories.StudentFactory')
    course = factory.SubFactory('app.factories.CourseFactory')
    session = factory.SubFactory('app.factories.SessionFactory')

# ReportCard Factory
class ReportCardFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Populate ReportCard table with random data for test 
    """
    class Meta:
        model = ReportCard
        sqlalchemy_session = db.session

    score = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=100))
    description = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=50))
    date = factory.LazyAttribute(lambda _: fake.date())

    teacher = factory.SubFactory('app.factories.TeacherFactory')
    student = factory.SubFactory('app.factories.StudentFactory')
    session = factory.SubFactory('app.factories.SessionFactory')
    assignment = factory.SubFactory('app.factories.AssignmentFactory')

# Progress Factory
class ProgressFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Populate Progress table with random data for test 
    """
    class Meta:
        model = Progress
        sqlalchemy_session = db.session

    description = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=50))
    date = factory.LazyAttribute(lambda _: fake.date())

    teacher = factory.SubFactory('app.factories.TeacherFactory')
    student = factory.SubFactory('app.factories.StudentFactory')
    course = factory.SubFactory('app.factories.CourseFactory')

# Score Factory
class ScoreFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Populate Score table with random data for test 
    """
    class Meta:
        model = Score
        sqlalchemy_session = db.session

    tag = factory.LazyAttribute(lambda _: fake.random_element(elements=tags))
    value = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=100))
    description = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=50))
    date = factory.LazyAttribute(lambda _: fake.date())

    assignment = factory.SubFactory('app.factories.AssignmentFactory')
