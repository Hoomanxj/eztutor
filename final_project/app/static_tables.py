from app import app, db  # Import app instance and db


def upsert_tag(name):
    """
    a function to update/insert values for Tag table population
    """
    from app.models import Tag

    tg = Tag.query.filter_by(name=name).first()
    if not tg:
        tg = Tag(name=name)
        db.session.add(tg)
        db.session.commit()  # Commit to catch any issues immediately


def populate_tag():
    """
    a function to populate Tag table with tags as values
    """
    from app.models import Tag, tags  # Ensure tags is defined

    for tag in tags:
        upsert_tag(tag)  # Call upsert_tag for each tag


def seed_data():
    """
    a function to initiate seed population of static tables
    """
    populate_weekday()
    populate_tag()


# Set up application context and run seeding process
with app.app_context():
    seed_data()
from app import app, db  # Import app instance and db

def upsert_weekday(name):
    """
    a function to update/insert values for Weekday table population
    """
    from app.models import Weekday

    wd = Weekday.query.filter_by(name=name).first()
    if not wd:
        wd = Weekday(name=name)
        db.session.add(wd)
        db.session.commit()  # Commit to catch any issues immediately


def populate_weekday():
    """
    a function to populate Weekday table with weekdays as values
    """
    from app.models import Weekday, week_day  # Ensure week_day is defined

    for day in week_day:
        upsert_weekday(day)  # Call upsert_weekday for each day


def upsert_tag(name):
    """
    a function to update/insert values for Tag table population
    """
    from app.models import Tag

    tg = Tag.query.filter_by(name=name).first()
    if not tg:
        tg = Tag(name=name)
        db.session.add(tg)
        db.session.commit()  # Commit to catch any issues immediately


def populate_tag():
    """
    a function to populate Tag table with tags as values
    """
    from app.models import Tag, tags  # Ensure tags is defined

    for tag in tags:
        upsert_tag(tag)  # Call upsert_tag for each tag


def seed_data():
    """
    a function to initiate seed population of static tables
    """
    populate_weekday()
    populate_tag()


# Set up application context and run seeding process
with app.app_context():
    seed_data()
