"""
app/forms.py

This module holds forms and handles form html rendering.
"""

from flask import render_template_string
from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, PasswordField, TextAreaField, IntegerField,
    SelectField, DateField, EmailField, SelectMultipleField,
    FileField, FieldList, TimeField
)
from wtforms.widgets import (
    ListWidget, CheckboxInput
)
from wtforms.validators import (
    DataRequired, InputRequired, URL, Email, Optional, EqualTo, Length
)
from app.queries import find_score_choices, find_tag
from app.choices import *


class RegisterUserForm(FlaskForm):
    """ user creation class """

    first_name = StringField('First Name',
                             validators=[InputRequired(), Length(max=50)])
    last_name = StringField('Last Name',
                            validators=[InputRequired(), Length(max=100)])
    date_of_birth = DateField('Date of Birth',
                              validators=[InputRequired()])
    gender = SelectField('Gender',
                         default="",
                         choices=gender_choices,
                         validators=[Optional()])
    email = EmailField('Email',
                       validators=[InputRequired(),
                                   Email(check_deliverability=True), Length(max=100)])
    cell = StringField('Cellphone Number',
                       default="",
                       validators=[Optional(), Length(max=60)])
    country = StringField('Country',
                          default="",
                          validators=[Optional(), Length(max=100)])
    city = StringField('City',
                       default="",
                       validators=[Optional(), Length(max=100)])
    address = TextAreaField('Address',
                            default="",
                            validators=[Optional()])
    education_level = SelectField('Education Level',
                                  choices=education_level_choices,
                                  validators=[InputRequired()])
    field_of_study = StringField('Field of Study',
                                 validators=[InputRequired(), Length(max=200)])
    native_language = StringField('Native Language',
                                  validators=[InputRequired(), Length(max=50)])
    teaching_language = StringField('Teaching Language',
                                    validators=[Optional()])
    learning_language = StringField('Learning Language',
                                    validators=[Optional()])
    password = PasswordField('Password',
                             validators=[InputRequired(), Length(min=8, max=32)])
    confirmation = PasswordField(
        'Confirmation',
        validators=[InputRequired(),
                    EqualTo('password',
                            message='Password does not match'), Length(min=8, max=32)])
    
    def render(self, user_type, gender_choices, education_level_choices):
        """ Render form for frontend """

        template = """
        <form id="dynamic-form" method="post" action="{{ url_for('auth.register_user') }}">
            {% from 'macros.html' import field %}
            {{ form.hidden_tag() }}
            <div class="border-4 border-amber-600">
                <div>
                    <h3 class="text-center">Personal</h3>
                </div>
                <div class="flex flex-wrap">
                    {{ field("first_name", "First Name", "text", placeholder="First Name", required=True, value=form.first_name.data or "", class_extra="w-full md:w-2/4 p-2") }}
                    {{ field("last_name", "Last Name", "text", placeholder="Last Name", required=True, value=form.last_name.data or "", class_extra="w-full md:w-2/4 p-2") }}
                </div>
                <div class="flex flex-wrap">
                    {{ field("date_of_birth", "Date of Birth", "date", placeholder="Date of Birth", required=True, value=form.date_of_birth.data or "2025-01-01", class_extra="w-full md:w-2/4 p-2") }}
                    {{ field("gender", "Gender", "select", choices=gender_choices, placeholder="Gender", required=False, value=form.gender.data or None, class_extra="w-full md:w-2/4 p-2") }}
                </div>
                <div>
                    <h3 class="text-center">Contact</h3>
                </div>
                <div class="flex flex-wrap">
                    {{ field("email", "Email", "email", placeholder="you@example.com", required=True, value=form.email.data or "", class_extra="w-full md:w-2/3 p-2") }}
                    {{ field("cell", "Cell Number", "text", placeholder="Cell Number", required=False, value=form.cell.data or "", class_extra="w-full md:w-1/3 p-2") }}
                </div>
                <div class="flex flex-wrap">
                    {{ field("country", "Country", "text", placeholder="Country", required=False, value=form.country.data or "", class_extra="w-full md:w-2/4 p-2") }}
                    {{ field("city", "City", "text", placeholder="City", required=False, value=form.city.data or "", class_extra="w-full md:w-2/4 p-2") }}
                </div>
                <div class="flex flex-wrap">
                    {{ field("address", "Address", "textarea", placeholder="Address", required=False, value=form.address.data or "", class_extra="w-full p-2") }}
                </div>
                <div>
                    <h3 class="text-center">Education</h3>
                </div>
                <div class="flex flex-wrap">
                    {{ field("education_level", "Education Level", "select", choices=education_level_choices, placeholder="Education Level", required=True, value=form.education_level.data or "", class_extra="w-full md:w-2/4 p-2") }}
                    {{ field("field_of_study", "Field of Study", "text", placeholder="Field of Study", required=True, value=form.field_of_study.data or "", class_extra="w-full md:w-2/4 p-2") }}
                </div>
                <div class="flex flex-wrap">
                    {{ field("native_language", "Native Language", "text", placeholder="What is your native language", required=True, value=form.native_language.data or "", class_extra="w-full md:w-2/4 p-2") }}
                    {% if user_type == 'teacher' %}
                        {{ field("teaching_language", "Teaching Language", "text", placeholder=" Language you are teaching", required=False, value=form.teaching_language.data or "", class_extra="w-full md:w-2/4 p-2") }}
                    {% elif user_type == 'student' %}
                        {{ field("learning_language", "Learning Language", "text", placeholder=" Language you are learning", required=False, value=form.learning_language.data or "", class_extra="w-full md:w-2/4 p-2") }}
                    {% endif %}
                </div>
                <div class="flex flex-wrap">
                    {{ field("password", "Password", "password", placeholder="Password", required=True, class_extra="w-full md:w-2/4 p-2") }}
                    {{ field("confirmation", "Confirmation", "password", placeholder="Confirmation", required=True, class_extra="w-full md:w-2/4 p-2") }}
                </div>
                <input id="hidden_input" type="hidden" name="form_type" value="register">
                <div class="flex justify-center">
                            <button type="submit" class="bg-gradient-to-r bg-amber-600 text-white px-4 py-2 rounded-full shadow-lg transition transform duration-500 hover:scale-110 hover:shadow-2xl">Submit</button>
                </div>
            </div>
        </form>
        """
        return render_template_string(template, form=self, user_type=user_type,
                                      gender_choices=gender_choices,
                                      education_level_choices=education_level_choices
                                      )


class CreateCourseForm(FlaskForm):
    """ create a new course"""
    
    student_email = EmailField('Student Email',
                               validators=[Optional(),
                                           Email(),
                                           Length(max=100)])
    name = StringField('Course Name',
                       validators=[InputRequired(),
                                   Length(max=100)])
    type = SelectField('Course Type',
                       choices=course_type_choices,
                       validators=[InputRequired()])
    format = SelectField('Course Format',
                         choices=course_format_choices,
                         validators=[InputRequired()])
    system = SelectField('Grading System',
                         choices=grading_system_choices,
                         validators=[InputRequired()])
    description = TextAreaField('Description',
                                validators=[DataRequired()])
    start_date = DateField('Start Date',
                           validators=[InputRequired()])
    start_hour = SelectField('Start time',
                             choices=time_choices,
                            validators=[
                                 InputRequired(),
                                 ])
    weekdays = SelectMultipleField('Weekdays',
                           choices=weekdays_choices,
                           widget=ListWidget(prefix_label=False),
                           option_widget=CheckboxInput(),
                           validators=[Optional()])
    number_of_session = IntegerField('Number of Sessions',
                                    validators=[DataRequired()])
    session_duration = SelectField('Session Duration',
                                    choices=session_duration_choices,
                                    validators=[DataRequired()])
    number_of_student = IntegerField('Number of Students',
                                     validators=[DataRequired()])
    
    link = StringField("Your online classroom link",
                       validators=[Optional(),
                                   URL(message="Invalid URL. Must start with http:// or https://")])
    submit = SubmitField('Create Course')

    def render(self, course_type_choices, course_format_choices,
               grading_system_choices, time_choices, weekdays_choices,
               session_duration_choices):
        """Render the HTML of the form"""
        template = """
        <form id="dynamic-form" method="post" action="{{ url_for('course.submit_form') }}">
            <div class="border-4 border-amber-600">
                {% from 'macros.html' import field %}
                {{ form.hidden_tag() }}
                <div class="flex flex-wrap p-2">
                    {{ field("name", "Course Name", "text", placeholder="Course Name", required=True, value=form.name.data or "", class_extra="w-full md:w-1/4 p-2") }}
                    {{ field("type", "Course Type", "select", choices=course_type_choices, placeholder="Select a Course Type", required=True, value=form.type.data or "", class_extra="w-full md:w-1/4 p-2") }}
                    {{ field("format", "Course Format", "select", choices=course_format_choices, placeholder="Select a Course Format", required=True, value=form.format.data or "", class_extra="w-full md:w-1/4 p-2") }}
                    {{ field("system", "Grading System", "select", choices=grading_system_choices, placeholder="Select a grading system", required=True, value=form.system.data or "", class_extra="w-full md:w-1/4 p-2") }}
                </div>
                <div class="flex flex-wrap items-center p-2">
                    {{ field("description", "Description", "textarea", placeholder="Description of the course...", required=True, value=form.description.data or "", class_extra="w-2/4 border rounded p-2") }}
                    {{ field("start_date", "Start Date", "date", placeholder="Choose a Start Date", required=True, value=form.start_date.data or "2025-01-01", class_extra="w-1/4 border rounded p-2") }}
                    {{ field("start_hour", "Start Hour", "select", choices=time_choices, placeholder="Select a Start Hour", required=True, value=form.start_hour.data or "14:00", class_extra="w-1/4 border rounded p-2") }}
                </div>
                <div class="flex justify-evenly items-center">
                    <!-- Weekdays as SelectMultipleField with Checkboxes -->
                    <div class="form-group mb-4">
                        <label for="{{ form.weekdays.id }}" class="block text-sm font-medium text-gray-700">
                            {{ form.weekdays.label.text }}
                        </label>
                        <div class="mt-2 flex flex-wrap">
                            {% for subfield in form.weekdays %}
                                <label class="inline-flex items-center mr-6">
                                    {{ subfield(class="form-checkbox h-4 w-4 text-amber-600") }}
                                    <span class="ml-2 text-gray-700">{{ subfield.label.text }}</span>
                                </label>
                            {% endfor %}
                        </div>
                        {% for error in form.weekdays.errors %}
                            <span class="text-red-500 text-sm">{{ error }}</span>
                        {% endfor %}
                    </div>
                </div>
                <div class="flex flex-wrap">
                    {{ field("number_of_session", "Number of Sessions", "integer", placeholder="Enter number of sessions", required=True, value=form.number_of_session.data or "", class_extra="w-1/3 border rounded p-2") }}
                    {{ field("session_duration", "Session Duration", "select", choices=session_duration_choices, placeholder="Select a session duration", required=True, value=form.session_duration.data or "", class_extra="w-1/3 border rounded p-2") }}
                    {{ field("number_of_student", "Number of Students", "integer", placeholder="Enter number of students", required=True, value=form.number_of_student.data or "", class_extra="w-1/3 border rounded p-2") }}
                </div>
                <div class="flex flex-wrap justify-center items-center">
                    {{ field("student_email", "Student Email", "email", placeholder="you@example.com", required=False, value="", class_extra="w-1/2 border rounded p-2") }}
                    {{ field("link", "Class Link", "url", placeholder="Your online classroom link", required=False, value="", class_extra="w-1/2 border rounded p-2") }}

                </div>
                <input id="hidden_input" type="hidden" name="form_type" value="create">
                <div class="flex justify-center">
                    <button type="submit" class="bg-gradient-to-r bg-amber-600 text-white px-4 py-2 rounded-full shadow-lg transition transform duration-500 hover:scale-110 hover:shadow-2xl">Create Course</button>
                </div>
            </div>
        </form>
        """
        return render_template_string(template, form=self,
                                      course_type_choices=course_type_choices,
                                      course_format_choices=course_format_choices,
                                      grading_system_choices=grading_system_choices,
                                      time_choices=time_choices,
                                      weekdays_choices=weekdays_choices,
                                      session_duration_choices=session_duration_choices)


class CreateAssignmentForm(FlaskForm):
    """ Create an assignment """

    session = StringField('Session',
                          validators=[InputRequired()])
    category = SelectField('Category',
                           choices=assignment_category_choices,
                           validators=[InputRequired()])
    description = TextAreaField('Description',
                                validators=[DataRequired()])
    start_date = DateField('Start Date',
                           validators=[InputRequired()])
    end_date = DateField('End Date',
                         default="",
                         validators=[Optional()])
    def render(self, category_choices):
        """ Render the html of form """
        template = """
        <form id="dynamic-form" method="post" action="{{ url_for('assignment.create_assignment') }}">
            {% from 'macros.html' import field %}
            {{ form.hidden_tag() }}
            <div class="border-4 border-amber-600 p-2">
                <div class="flex flex-wrap">
                    {{ field("session", "Session", "text", placeholder="Enter a session", required=True, class_extra="w-full md:w-1/2") }}
                    {{ field("category", "Category", "select", choices=category_choices, placeholder="Select a Category", required=True, class_extra="w-full md:w-1/2") }}
                </div>
                <div class="flex flex-wrap">
                    {{ field("start_date", "Start Date", "date", placeholder="Choose a Start Date", required=True, class_extra="w-full md:w-1/2") }}
                    {{ field("end_date", "End Date", "date", placeholder="Choose an End Date", class_extra="w-full md:w-1/2") }}
                </div>
                <div class="flex flex-wrap">
                    {{ field("description", "Description", "textarea", placeholder="Description of the assignment...", required=True, class_extra="w-full") }}
                </div>
                
                
                <input id=hidden_input type="hidden" name="form_type" value="create">
                <div class="flex justify-center">
                    <button type="submit" class="bg-gradient-to-r bg-amber-600 text-white px-4 py-2 rounded-full shadow-lg transition transform duration-500 hover:scale-110 hover:shadow-2xl">Create Assignment</button>
                </div>
            </div>
        </form>
        """
        return render_template_string(template, form=self, category_choices=category_choices)


def dynamic_create_assignment():
    """ Pass the choices to the form and render """

    form = CreateAssignmentForm()
    form.category.choices=assignment_category_choices

    return form    


class CreateFeedbackForm(FlaskForm):
    """ Create feedback for progress """

    student = SelectField('Student',
                          validators=[InputRequired()])
    description = TextAreaField('Description',
                                validators=[DataRequired()])


class LoginForm(FlaskForm):
    """ Login user """

    email = EmailField('Email',
                       validators=[InputRequired()])
    password = PasswordField('password',
                             validators=[InputRequired()])
    user_type = SelectField('Login As',
                            choices=user_type_choices)
    
    def render(self, user_type_choices):
        """ Render form in html """
        template = """
        <form id="dynamic-form" method="post" action="{{ url_for('auth.log_user_in') }}">
            {% from 'macros.html' import field %}
            {{ form.hidden_tag() }}
            {{ field("user_type", "Login as", "select", choices=user_type_choices, placeholder="Select a User Type", required=True, value=form.user_type.data or "") }}
            {{ field("email", "Email", "email", placeholder="you@example.com") }}
            {{ field("password", "Password", "password", placeholder="Password", required=True) }}
            <div class="flex justify-center items-center">
                <button type="submit" class="bg-gradient-to-r bg-amber-600 text-white px-4 py-2 rounded-full shadow-lg transition transform duration-500 hover:scale-110 hover:shadow-2xl">Login</button>
            </div>
        </form>
        """
        return render_template_string(template, form=self,
                                      user_type_choices=user_type_choices)


class SubmitAssignmentForm(FlaskForm):
    """ Attaching assignments file to email """

    file = FileField("Attach your file here",
                     validators=[Optional()])
    description = TextAreaField("Note",
                                validators=[Optional()])
    submit = SubmitField('Submit assignment')

    def render(self):
        """ Render the html of form """
        
        template = """
        <form id="dynamic-form" method="post" action="{{ url_for('assignment.submit_assignment') }}">
            {% from 'macros.html' import field %}
            {{ form.hidden_tag() }}
            <div class="border-4 border-amber-600 p-2">
                {{ field("file", "Upload File", "file", placeholder="Upload your file here") }}
                {{ field("description", "Description", "textarea", placeholder="Description of the assignment...", required=True) }}
                <input id=hidden_input type="hidden" name="form_type" value="submit">
                <div class="flex justify-center items-center">
                    <button type="submit" class="bg-gradient-to-r bg-amber-600 text-white px-4 py-2 rounded-full shadow-lg transition transform duration-500 hover:scale-110 hover:shadow-2xl">Submit Assigment</button>
                </div>
            </div>
        </form>
        """
        return render_template_string(template, form=self)


class ScoreAssignmentForm(FlaskForm):
    """ Score assignments using tags """

    score = FieldList(SelectField('Score',
                        choices=[],
                        coerce=int,
                        validators=[
                        InputRequired()
                      ]))
    description = FieldList(TextAreaField('Description',
                              validators=[
                                  Optional()
                              ]))
    
    def render(self,pairs,system_type):
        """ Render the html of form """
        template = """
            <form id="dynamic-form" method="post" action="{{ url_for('assignment.score_assignment') }}">
                {% from 'macros.html' import field %}
                {{ form.hidden_tag() }}
                <div class="flex justify-center flex-wrap gap-4">
                    {% for tag, score_field, desc_field in pairs %}
                        <!-- Each group is a grid item -->
                        <div class="flex flex-col items-center border-2 border-amber-600 rounded-lg p-6 mx-4">
                            <!-- Label centered at the top -->
                            <label class="block font-medium text-center mb-4 text-lg">{{ tag }}</label>
                            <!-- Score and Description side by side -->
                            <div class="flex items-center space-x-4 w-full">
                                {{ field(score_field.name, type="select", choices=score_field.choices, placeholder="Score") }}
                                {{ field(desc_field.name, type="textarea", placeholder="Description") }}
                            </div>
                        </div>
                    {% endfor %}
                </div>
                <input id="hidden_input" type="hidden" name="form_type" value="score">
                <input type="hidden" name="system" value="{{ system_type }}">
                <div class="flex justify-center items-center mt-4">
                    <button type="submit" class="bg-gradient-to-r bg-amber-600 text-white px-4 py-2 rounded-full shadow-lg transition transform duration-500 hover:scale-110 hover:shadow-2xl">Submit Scores</button>
                </div>
            </form>

        """
        return render_template_string(template, form=self, pairs=pairs, system_type=system_type)


def dynamic_score_assignment(course_id, assignment_id):
    """ Pass the choices to the form and render """

    form = ScoreAssignmentForm()
    system_type, score_choices, success = find_score_choices(int(course_id))
    tags, success = find_tag(int(assignment_id))
    form.score.choices = score_choices

    tags = [t[1] for t in tags]
    for _ in tags:
        form.score.append_entry()
        form.score.entries[-1].choices = score_choices  # Ensure this entry gets the choices
        form.description.append_entry()

    pairs = list(zip(tags, form.score, form.description))

    return form, pairs, system_type


class SessionSelectForm(FlaskForm):
    """ A single-field from for session page """
    
    course = SelectField('Course',
                         choices=[],
                         validators=[InputRequired()])


class UpdateSessionForm(FlaskForm):
    """ A form to update sessions in session page """

    type = SelectField("Type",
                       choices=session_type_choices)
    status = SelectField("Status",
                         choices=session_status_choices)
    date = DateField("Date", format='%Y-%m-%d')
    day = SelectField("Day",
                      choices=session_day_choices)
    duration = IntegerField("Duration")
    description = StringField("Description")

    def render(self,user_type, session_id, session_type_choices, session_status_choices,
               session_day_choices, session_duration_choices):
        """ render for front-end """
        template = """
        {% if user_type == "teacher" %}
        <form  @submit.prevent="updateSession()" id="invite-student-form" method="post" action="{{ url_for('session.update_session_info') }}">
            <div class="border-4 border-amber-600 p-2">
                {% from 'macros.html' import field %}
                {{ form.hidden_tag() }}
                <div class="flex flex-wrap justify-evenly items-center">
                    {{ field("type", "Type", "select", choices=session_type_choices, placeholder="Select a type", required=False, value=form.type.data or "", class_extra="w-full md:w-1/3") }}
                    {{ field("status", "Status", "select", choices=session_status_choices, placeholder="Select a status", required=False, value=form.status.data or "", class_extra="w-full md:w-1/3") }}
                    {{ field("date", "Date", "date", placeholder="Choose a Date", required=False, value=form.date.data or "2025-01-01", class_extra="w-full md:w-1/3") }}
                </div>
                <div class="flex flex-wrap justify-evenly">
                    {{ field("day", "Day", "select", choices=session_day_choices, placeholder="Select a day", required=False, value=form.day.data or "", class_extra="w-full md:w-1/2") }}
                    {{ field("duration", "Duration", "select", choices=session_duration_choices, placeholder="Select a duration", required=False, value=form.duration.data or 45, class_extra="w-full md:w-1/2") }}
                </div>
                <div class="flex flex-wrap justify-evenly">
                    {{ field("description", "Description", "textarea", placeholder="Session notes...", required=False, value=form.description.data or "", class_extra="w-full") }}
                </div>
                <input type="hidden" name="session_id" value="{{ session_id }}">
                <div class="flex justify-center">
                    <button type="submit" class="bg-gradient-to-r bg-amber-600 text-white px-4 py-2 rounded-full shadow-lg transition transform duration-500 hover:scale-110 hover:shadow-2xl">Update Session</button>
                </div>
            </div>
        </form>
        {% elif user_type == "student" %}
        <div class="container grid grid-cols-3 p-2 shadow-md border-4 border-amber-600">
            <div class="grid grid-cols-1 p-2">
                <div x-text="'Type: ' + '{{ form.type.data }}'"></div>
                <div x-text="'Status: ' + '{{ form.status.data }}'"></div>
            </div>
            <div class="grid grid-cols-1 p-2">
                <div x-text="'Date: ' + '{{ form.date.data }}'"></div>
                <div x-text="'Duration: ' + '{{ form.duration.data }}'" class="w-full md:w-1/2"></div>
            </div>
            <div class="grid grid-cols-1 p-2 place-items-center">
                <div x-text="'Description: ' + '{{ form.description.data }}'" class="w-full"></div>
            </div>
        </div>
        {% endif %}
        """
        return render_template_string(template, form=self,
                                      user_type=user_type,
                                      session_id=session_id,
                                      session_type_choices=session_type_choices,
                                      session_status_choices=session_status_choices,
                                      session_day_choices=session_day_choices,
                                      session_duration_choices=session_duration_choices,
                                    )


class AddTaskForm(FlaskForm):
    """ A form for custom tasks """

    task = StringField("Task Name",
                       validators=[InputRequired()])
    time_from = TimeField("Starting at",
                          validators=[InputRequired()])
    time_to = TimeField("Ending at",
                        validators=[InputRequired()])

    def render(self):
        """ render for front-end """
        template = """
        <form id="add-task-form" method="post" action="{{ url_for('calendar.add_task') }}">
            {% from 'macros.html' import field %}
            {{ form.hidden_tag() }}
            {{ field("task", "Task", "text", placeholder="Name of the Task", required=True) }}
            {{ field("time_from", "Starting from", "time", placeholder="From", required=True, min="00:00", max="23:59") }}
            {{ field("time_to", "Ending at", "time", placeholder="To", required=True, min="00:00", max="23:59") }}
            <button type="submit" class="bg-gradient-to-r bg-amber-600 text-white px-4 py-2 rounded-full shadow-lg transition transform duration-500 hover:scale-110 hover:shadow-2xl">Submit</button>
        </form>
        """
        return render_template_string(template, form=self)


class inviteForm(FlaskForm):
    """ A form to invite students to a course """

    email = EmailField("Email",
                       validators=[InputRequired(),
                                   Email(),
                                   Length(max=100)])

    def render(self, course_id):
        """ render for front-end """
        template = """
        <form id="invite-student-form" method="post" action="{{ url_for('course.send_invitation') }}">
            {% from 'macros.html' import field %}
            {{ form.hidden_tag() }}
            <div class="flex">
            {{ field("email", "Email", "email", placeholder="you@example.com", required=True, class_extra="w-full p-2") }}
            </div>
            <input type="hidden" name="course_id" value="{{ course_id }}">
            <div class="flex justify-center">
                <button type="submit" class="bg-gradient-to-r bg-amber-600 text-white px-4 py-2 rounded-full shadow-lg transition transform duration-500 hover:scale-110 hover:shadow-2xl">Invite</button>
            </div>
        </form>
        """
        return render_template_string(template, form=self, course_id=course_id)