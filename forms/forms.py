from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import URL, DataRequired, Length, EqualTo


## creating forms to handle login and new registration

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class Registerform(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('lask Name', validators=[DataRequired()])
    mobile_number = StringField('Mobile number', validators=[DataRequired(), Length(11)])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Create Password', validators=[DataRequired()])
    confirm_password = StringField('Create Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
