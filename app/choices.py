"""
app/choices.py

This module holds all the choices used in forms and tables
"""


gender_choices = [("male", "Male"), ("female", "Female"), ("other", "Other")]

education_level_choices = [("high school or less", "High School or Less"), ("college", "College"),
                           ("bachelor's", "Bachelor's"), ("master's", "Master's"), ("doctoral", "Doctoral")]

course_type_choices = [("online", "Online"), ("on-site", "On-site")]

course_format_choices = [("private", "Private"), ("group", "Group")]

course_status_choices = ["ongoing", "concluded"]

grading_system_choices = [("numeric", "Numeric"), ("descriptive", "Descriptive")]

weekdays_choices = [("monday", "Monday"), ("tuesday", "Tuesday"), ("wednesday", "Wednesday"),
                    ("thursday", "Thursday"), ("friday", "Friday"), ("saturday", "Saturday"),
                    ("sunday", "Sunday")]

assignment_category_choices = [("speaking", "Speaking"), ("listening", "Listening"),
                               ("writing", "Writing"), ("reading", "Reading")]

grading_scores = [
    {"value": 0, "label": "No Attempt"}, {"value": 1, "label": "Failing"},
    {"value": 2, "label": "Very Poor"}, {"value": 3, "label": "Poor"},
    {"value": 4, "label": "Weak Pass"}, {"value": 5, "label": "Mediocre"},
    {"value": 6, "label": "Satisfactory"}, {"value": 7, "label": "Above Average"},
    {"value": 8, "label": "Good"}, {"value": 9, "label": "Very Good"},
    {"value": 10, "label": "Excellent"},
]

numeric_score_choices = [(c['value'], c['value']) for c in grading_scores]

descriptive_score_choices = [(c['value'], c['label']) for c in grading_scores]

session_type_choices = [("normal", "Normal"), ("makeup", "Makeup")]

session_status_choices = [("pending", "Pending"), ("held", "Held"), ("cancelled", "Cancelled")]

session_day_choices = [("monday", "Monday"), ("tuesday", "Tuesday"),
                       ("wednesday", "Wednesday"), ("thursday", "Thursday"),
                       ("friday", "Friday"), ("saturday", "Saturday"),
                       ("sunday", "Sunday")]

session_duration_choices = [(30, "30"), (45, "45"), (60, "60"), (75, "75"), (90, "90"),
                            (105, "105"), (120, "120")]

user_type_choices = [("teacher", "Teacher"), ("student", "Student")]

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

def populate_hour():
    """
    Create a list of options be used for hours of courses
    
    Args:
        -None
    
    Returns:
        -class_start_hour: options
    """

    class_start_hour = []
    minutes = ["00", "15", "30", "45"]
    time = ""
    for i in range(3):
        for j in range(10):
            for m in minutes:
                if time != "23:45:00": # To stop it from surpassing 24 hours
                    time = f"{i}{j}:{m}:00"
                    label = f"{i}{j}:{m}"
                    t = (time,label)
                    class_start_hour.append(t)
                else:
                    break
    return class_start_hour

# Store time choice options
time_choices = populate_hour()
