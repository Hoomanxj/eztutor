from app import create_app, db  # Import your app and db instance
from app.factories import TeacherFactory, StudentFactory, CourseFactory, SessionFactory, AttendanceFactory, AssignmentFactory, ReportCardFactory, ProgressFactory, ScoreFactory

# Initialize the Flask app
app = create_app()  # Replace with your app initialization method
app.app_context().push()  # Push an application context if needed

# Create the database tables (use a test database to avoid affecting production data)
db.create_all()

# Generate and commit data using factories
teacher = TeacherFactory.create()  # This creates and saves a Teacher instance
student = StudentFactory.create()  # This creates and saves a Student instance
course = CourseFactory.create(teacher=teacher)  # Creates a Course with the teacher
session = SessionFactory.create(course=course, teacher=teacher, student=student)  # Creates a Session with the course, teacher, and student
attendance = AttendanceFactory.create(session=session, student=student)  # Creates Attendance for a student in the session
assignment = AssignmentFactory.create(course=course, teacher=teacher, student=student, session=session)  # Creates an Assignment for the student
report_card = ReportCardFactory.create(assignment=assignment, student=student, teacher=teacher, session=session)  # Creates a ReportCard
progress = ProgressFactory.create(course=course, student=student, teacher=teacher)  # Creates Progress for the student
score = ScoreFactory.create(assignment=assignment)  # Creates a Score for the assignment

db.session.commit()

# Verify data has been added (you can query or print the objects)
print(teacher.first_name, teacher.email)
print(student.first_name, student.email)
print(course.name)
print(session.date)
print(attendance.status)
print(assignment.description)
print(report_card.score)
print(progress.description)
print(score.value)

