from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired
from wtforms import validators, ValidationError

class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    id_num = StringField('ID Number', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    email = StringField("Email",[validators.Required("Please enter your email address."),
      validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    acctype = SelectField('Account Type', choices=[('leader', 'Project Leader'), ('member', 'Club Member')], validators=[InputRequired()])
    special_interest_group=SelectField('Special interest group',
    choices=[('mobile', 'Mobile App Development'), ('robot', 'Robotics'),('security', 'Cyber Security'),
    ('games', 'Game Development'),('web', 'Web Development')],validators=[InputRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class MessageForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    message = TextAreaField('Message', validators=[InputRequired()])
    
class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired()])
    sig = =SelectField('Special interest group',
    choices=[('mobile', 'Mobile App Development'), ('robot', 'Robotics'),('security', 'Cyber Security'),
    ('games', 'Game Development'),('web', 'Web Development')], validators=[InputRequired()])

class TaskForm(FlaskForm):
    assignee = StringField('Assignee Name')
    projectname = StringField('Project Name', validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired()])