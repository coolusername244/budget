from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

# create registration form
class RegistrationForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=4, max=30)])
    password = PasswordField(validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField(validators=[
        DataRequired(),
        EqualTo("password", message="Password and Confirmation must match")])
    submit = SubmitField("Register!")

# create log in form
class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField("Log In")
