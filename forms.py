from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, SelectMultipleField, PasswordField,\
    TextAreaField, validators, widgets
from models import Projects, Topics
from app import db

## define MultiCheckboxField - https://gist.github.com/doobeh/4668212
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

## form to add project
class ProjectForm(FlaskForm):
    name = StringField(label = "Give Your Project a Name:", validators=[validators.DataRequired()])
    summary = TextAreaField(label = "Brief Description:")
    submit = SubmitField(label="Add Project")

## form to add book source
class BookForm(FlaskForm):
    project = SelectField(label = "Select Project",
                          choices = [])
    title = StringField(label="Book Title",
                        validators=[validators.DataRequired()])
    person_type = SelectField(label = "Add Contributers", choices=['author', 'editor', 'translator'])
    person_first = StringField(render_kw={'placeholder': 'first'}, default=None)
    person_middle = StringField(render_kw={'placeholder': 'middle'}, default=None)
    person_last = StringField(render_kw={'placeholder': 'last'}, default=None)
    ## optional additional contributers
    second_person_type = SelectField(choices=['author', 'editor', 'translator'])
    second_person_first = StringField(render_kw={'placeholder': 'first'}, default="")
    second_person_middle = StringField(render_kw={'placeholder': 'middle'}, default="")
    second_person_last = StringField(render_kw={'placeholder': 'last'}, default="")

    third_person_type = SelectField(choices=['author', 'editor', 'translator'])
    third_person_first = StringField(render_kw={'placeholder': 'first'}, default="")
    third_person_middle = StringField(render_kw={'placeholder': 'middle'}, default="")
    third_person_last = StringField(render_kw={'placeholder': 'last'}, default="")

    fourth_person_type = SelectField(choices=['author', 'editor', 'translator'])
    fourth_person_first = StringField(render_kw={'placeholder': 'first'}, default="")
    fourth_person_middle = StringField(render_kw={'placeholder': 'middle'}, default="")
    fourth_person_last = StringField(render_kw={'placeholder': 'last'}, default="")

    fifth_person_type = SelectField(choices=['author', 'editor', 'translator'])
    fifth_person_first = StringField(render_kw={'placeholder': 'first'}, default="")
    fifth_person_middle = StringField(render_kw={'placeholder': 'middle'}, default="")
    fifth_person_last = StringField(render_kw={'placeholder': 'last'}, default="")

    publisher = StringField(label = "Book Publisher")
    year = IntegerField(label="Year of Publication")
    edition = IntegerField(label="Book Edition")
    volume = IntegerField(label="Book Volume")
    section = StringField(label="Book Section (e.g. chapter title)")
    description = TextAreaField(label="Brief Description of Source")
    submit= SubmitField(label="Add Book")

## form to add periodical source
class PeriodicalForm(FlaskForm):
    project = SelectField(label = "Select Project",
                          choices = [])
    title = StringField(label="Article Title",
                        validators=[validators.DataRequired()])
    person_type = SelectField(label = "Add Contributers", choices=['author', 'editor', 'translator'])
    person_first = StringField(render_kw={'placeholder': 'first'}, default=None)
    person_middle = StringField(render_kw={'placeholder': 'middle'}, default=None)
    person_last = StringField(render_kw={'placeholder': 'last'}, default=None)
    ## optional additional contributers
    second_person_type = SelectField(choices=['author', 'editor', 'translator'])
    second_person_first = StringField(render_kw={'placeholder': 'first'}, default="")
    second_person_middle = StringField(render_kw={'placeholder': 'middle'}, default="")
    second_person_last = StringField(render_kw={'placeholder': 'last'}, default="")

    third_person_type = SelectField(choices=['author', 'editor', 'translator'])
    third_person_first = StringField(render_kw={'placeholder': 'first'}, default="")
    third_person_middle = StringField(render_kw={'placeholder': 'middle'}, default="")
    third_person_last = StringField(render_kw={'placeholder': 'last'}, default="")

    fourth_person_type = SelectField(choices=['author', 'editor', 'translator'])
    fourth_person_first = StringField(render_kw={'placeholder': 'first'}, default="")
    fourth_person_middle = StringField(render_kw={'placeholder': 'middle'}, default="")
    fourth_person_last = StringField(render_kw={'placeholder': 'last'}, default="")

    fifth_person_type = SelectField(choices=['author', 'editor', 'translator'])
    fifth_person_first = StringField(render_kw={'placeholder': 'first'}, default="")
    fifth_person_middle = StringField(render_kw={'placeholder': 'middle'}, default="")
    fifth_person_last = StringField(render_kw={'placeholder': 'last'}, default="")

    journal = StringField(label = "Periodical Name (e.g. Journal, Magazine, Newspaper)",
                          validators=[validators.DataRequired()])
    volume = IntegerField(label = "Periodical Volume")
    issue = IntegerField(label = "Periodical Issue")
    month = SelectField(label = "Month of Publication",
                        choices = ["", "January", "February", "March", "April", "May", "June",
                                   "July", "August", "September", "October", "November", "December"])
    year = IntegerField(label = "Year of Publication")
    description = TextAreaField(label = "Brief Description of Source")
    submit = SubmitField(label = "Add Periodical")

## form to add subtopic
class SubtopicForm(FlaskForm):
    name = StringField(label = "Give your Subtopic a Name: ")
    submit = SubmitField(label = "Add Subtopic")

## form to add note
class NoteForm(FlaskForm):
    note = TextAreaField(label = "Type your note here")
    first_page = IntegerField(label = "Page range of note (if applicable)")
    last_page = IntegerField()
    topic = MultiCheckboxField(label = "What subtopic(s) is this note related to?",
                        choices = [])
    submit = SubmitField(label = "Add Note")

# registration form
class RegistrationForm(FlaskForm):
  name = StringField(label = 'Name', validators=[validators.DataRequired()])
  email = StringField(label = 'Email', validators=[validators.DataRequired(), validators.Email()])
  password = PasswordField(label = 'Password', validators=[validators.DataRequired()])
  password2 = PasswordField(label = 'Confirm Password',
                            validators = [validators.DataRequired(), validators.EqualTo('password')])
  submit = SubmitField(label = 'Register')

# sign-in form
class SignInForm(FlaskForm):
    email = StringField(label = "Email", validators = [validators.DataRequired()])
    password = PasswordField(label = "Password", validators = [validators.DataRequired()])
    submit = SubmitField(label = "SignIn")

# search form
class SearchForm(FlaskForm):
    text = StringField(validators = [validators.DataRequired()])
    search_submit = SubmitField(label = "Search")

class AdvancedSearchForm(FlaskForm):
    note_text = StringField(label = "Search Note Text")
    source_title_text = StringField(label = "Search Source Title")
    source_person_text = StringField(label = "Search Source Contributers (authors, editors, etc.)")
    source_type = MultiCheckboxField(label = "Select Source Type(s)")
    source_year_begin = IntegerField(label = "Select Year Range of Source Publication")
    source_year_end = IntegerField()
    project = SelectField(label = "Select Project(s)")
    subtopic = SelectField(label = "Select Subtopic(s)")
    submit = SubmitField(label = "Search")
