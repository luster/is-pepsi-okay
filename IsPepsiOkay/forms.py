from flask.ext.wtf import Form
from wtforms import validators
from wtforms import BooleanField, TextField, PasswordField, IntegerField, SelectField, HiddenField, DateField
from flask.ext.login import current_user
from IsPepsiOkay import database

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=3, max=40)])
    email = TextField('Email Address', [validators.Length(min=3, max=40)])
    password = PasswordField('Password', [validators.Length(min=6, max =40), validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Enter Password Again')
    dob = DateField('Date of Birth (YYYY-MM-DD)')

class ChangePasswordForm(Form):
    oldPassword = PasswordField('Password', [validators.Required()])
    password = PasswordField('Password', [validators.Length(min=6, max=40), validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Enter Password Again')

class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=3, max=40)])
    password = PasswordField('Password', [validators.Required()])
