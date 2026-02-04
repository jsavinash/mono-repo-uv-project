"""
forms/auth.py ─ Login & Registration WTForms.
"""

from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    first_name = StringField(
        "First Name",
        validators=[
            DataRequired(),
            Length(min=2, max=80, message="First name must be 2–80 characters."),
        ],
    )
    last_name = StringField(
        "Last Name",
        validators=[
            DataRequired(),
            Length(min=2, max=80, message="Last name must be 2–80 characters."),
        ],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Please enter a valid email.")],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters."),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Please enter a valid email.")],
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")
