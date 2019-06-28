from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url, Email, Regexp, Length, EqualTo
from wtforms import ValidationError



class BookmarkForm(FlaskForm):
    url = URLField('The URL for your bookmark:', validators=[DataRequired(), url()])
    description = StringField('Add an optional description:')
    tags = StringField('Tags', validators=[Regexp(r'^[a-zA-Z0-9, ]*$',                 
                    message="Tags can only contain letters and numbers")])


   
    def validate(self):
        if not self.url.data.startswith("http://") or\
            self.url.data.startswith("https://"):
            self.url.data = "http://" + self.url.data

        if not FlaskForm.validate(self):
            return False

        if not self.description.data:
            self.description.data = self.url.data

        #  filter out empty and duplicate tag names
        stripped = [t.strip() for t in self.tags.data.split(',')]
        not_empty = [tag for tag in stripped if tag]
        tagset = set(not_empty)
        self.tags.data = ",".join(tagset)

        return True

class LoginForm(FlaskForm):
    username = StringField('Your Username: ', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

from my_project import models

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
    Email()])

    username = StringField('Username', validators=[
    DataRequired(), Length(1, 64),
    Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
    'Usernames must have only letters, numbers, dots or '
    'underscores')])

    password = PasswordField('Password', validators=[
    DataRequired(), EqualTo('password2', message='Passwords must match.')])
    
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if models.User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if models.User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')