from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import *


def all_students(session):
    return session.query(Student).all()

if __name__ == "__main__":
    # Set up database engine (replace with your database URI)
    DATABASE_URL= 'mysql+pymysql://root:Whoman946626@localhost/eztutor'
    engine = create_engine(DATABASE_URL)

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()


students = all_students(session)
for student in students:
    print(student.id)
