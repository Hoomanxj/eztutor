"""
app/dataload.py

This module handles basic data load mainly for development purposes.
"""

import pycountry
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from app.extentions import db
from app.models import Student, Course, Assignment, Session, TagCategory

###################################################################################
# Below functions only have development values and are not used in project directly
###################################################################################


def populate_user():
    from app import create_app
    app = create_app()
    with app.app_context():
        teacher = Student(
            first_name="doodool",
            last_name="jafari",
            date_of_birth="1992/08/03",
            gender="male",
            email="cyclethecycle@gmail.com",
            cell="+989366911497",
            country="iran",
            city="tehran",
            address="somewhere",
            education_level="master's",
            field_of_study="industrial engineering",
            native_language="persian",
            learning_language="english",
            password_hash= generate_password_hash("Whoman946626@")
        )
        db.session.add(teacher)
        db.session.commit()


def populate_course():
    """ create courses"""
    from app import create_app
    app = create_app()
    with app.app_context():
        new_course = Course(
            teacher_id=1,
            name="English-preintermediate",
            type="online",
            format="private",
            description="a course for preintermediate level students",
            start_date="2024/08/03",
            end_date="2024/09/03",
            start_hour="14:00",
            number_of_session=8,
            session_duration=45,
            number_of_student=1
        )
        db.session.add(new_course)
        db.session.commit()


def populate_assignment():
    """ Populate assignments of different status """
    from app import create_app
    app = create_app()
    with app.app_context():
        new_assignment = Assignment(
            teacher_id=1,
            course_id=14,
            session_id=46,
            status="submitted".lower(),
            category="speaking",
            description="record your voice",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=3)
        )
        db.session.add(new_assignment)
        db.session.commit()


def initialize_description_empty():
    """ pass empty string to descriptions to prevent null value """
    from app import create_app
    app = create_app()
    with app.app_context():
        try:
            query = db.session.query(Session).all()
            for _ in query:
                _.description = ""
                db.session.add(_)
                db.session.commit()
            return "success"
        except Exception as e:
            db.session.rollback()
            return(f"Error: {e}")
            

def populate_tags():
    """ A function to populate tags for Tag table """
    from app import create_app
    app = create_app()
    with app.app_context():
        tags = [
            {"tag": "lexical resources", "category": "speaking", "description": "user's vocabulary range and level"},
            {"tag": "grammatical range", "category": "speaking", "description": "user's grammar range and accuracy"},
            {"tag": "task achievement", "category": "speaking", "description": "how successfully and directly they address the questions or prompts"},
            {"tag": "coherence", "category": "speaking", "description": "connectedness of ideas in language production"},
            {"tag": "cohesion", "category": "speaking", "description": "connectedness of ideas in represented by words and grammatical structures utilized"},
            {"tag": "pronunciation", "category": "speaking", "description": "the accuracy of pronunciation and accent"},
            {"tag": "fluency", "category": "speaking", "description": "language production without pauses and hesitations"},
            {"tag": "lexical resources", "category": "writing", "description": "user's vocabulary range and level"},
            {"tag": "grammatical range", "category": "writing", "description": "user's grammar range and accuracy"},
            {"tag": "task achievement", "category": "writing", "description": "how successfully and directly they address the questions or prompts"},
            {"tag": "coherence", "category": "writing", "description": "connectedness of ideas in language production"},
            {"tag": "cohesion", "category": "writing", "description": "connectedness of ideas in represented by words and grammatical structures utilized"},
            {"tag": "task achievement", "category": "listening", "description": "how successfully and directly they address the questions or prompts"},
            {"tag": "comprehension", "category": "listening", "description": "user's success in understanding the context of language received"},
            {"tag": "task achievement", "category": "reading", "description": "how successfully and directly they address the questions or prompts"},
            {"tag": "comprehension", "category": "reading", "description": "user's success in understanding the context of language received"}
        ]
        try:
            for tag in tags:
                new_tag = TagCategory(
                    tag=tag["tag"],
                    category=tag["category"],
                    description=tag["description"]
                )
                db.session.add(new_tag)
            db.session.commit()
            return "success"
        except Exception as e:
            db.session.rollback()
            return f"Dataload failed: {e}"


if __name__ == "__main__":
    print(populate_tags())

