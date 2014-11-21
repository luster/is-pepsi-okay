from flask.ext.wtf import (Form, BooleanField, TextField, PasswordField, IntegerField, SelectField, validators, HiddenField)
from flask.ext.login import current_user
from IsPepsiOk import database

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=6, max=40)])
    email = TextField('Email Address', [validaors.Length(min=6, max=40)])
    password = PasswordField('Password', [validators.Length(min=6, max =40), validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Enter Password Again')
    
class ChangePasswordForm(Form):
    oldPassword = PasswordField('Password', [validators.Required()])
    password = PasswordFeild('Password', [validators.Length(min=6, max=40), validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Enter Password Again')
    
class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=6, max=40)])
    password = PasswordField('Password', [validators.Required()])
