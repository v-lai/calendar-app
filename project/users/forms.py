from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  location = StringField('Location')
  password = PasswordField('Password', [
    validators.DataRequired(),
    validators.Length(min=6),
    validators.EqualTo('confirm', message='Passwords must match.')
  ])
  confirm = PasswordField('Confirm Password')

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[Length(min=6)])  
