from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired
from wtforms import validators, ValidationError

class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    email = StringField("Email",[validators.Required("Please enter your email address."),
      validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class MessageForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    message = TextAreaField('Message', validators=[InputRequired()])

class TrashForm(FlaskForm):
    trash_type=StringField('Type of Trash', validators=[InputRequired()])
    username = StringField('username', validators=[InputRequired()])