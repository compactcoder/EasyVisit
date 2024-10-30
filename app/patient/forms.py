from collections.abc import Mapping, Sequence
from typing import Any
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField,FloatField,TextAreaField, ValidationError
from wtforms.validators import DataRequired,Length, Email, Optional,EqualTo,Regexp, ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user

from app.models import PatientModel,UserModel


# Patient Registration Form
class PatientRegistrationForm(FlaskForm):
    full_name = StringField("Full Name",validators=[DataRequired(), Length(min=2, max=40)])
    email = StringField("Email",validators =[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=2, max=20)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField("Sign Up")
    
    # Emaiil validation in database
    def validate_email(self,email):
        patient = UserModel.query.filter_by(email=email.data,role="patient").first()
        if patient:
            raise ValidationError("Patient with this email is already registered.")

# Patient Login Form
class PatientLoginForm(FlaskForm):
    email = StringField("Email",validators =[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=2, max=20)])
    submit = SubmitField("Login")

# Patient Profile Update Form
class PatientProfileUpdateForm(FlaskForm):
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    #mandatory fields
    phone_no = StringField('Phone Number', validators=[DataRequired(),Length(min=10, max=10, message='Mobile number must be 10 digits long'),Regexp(r'^[6789]\d{9}$', message='Invalid mobile number format')])
    age = FloatField("Age",validators=[DataRequired()])
    gender = SelectField("Gender",choices=[("male","Male"),("female","Female")],validators=[DataRequired()])
    address = TextAreaField("Adress",validators=[DataRequired(),Length(max=200)])

    #optional fields
    height = FloatField("Height",validators=[Optional()])
    weight =FloatField("Weight", validators=[Optional()])

    submit = SubmitField("Update Profile")

    # #email validation check
    # def validate_email(self, email):
    #     if email.data != current_user.email:
    #         user = UserModel.query.filter_by(email=email.data,role="patient").first()
    #         if user:
    #             raise ValidationError('That email is taken. Please choose a different one.')
class PatientGetResetLinkForm(FlaskForm):
    email = StringField("Email",validators =[DataRequired(), Email()])
    submit = SubmitField("Get Password Reset Link")
    
    # Emaiil validation in database
    def validate_email(self,email):
        patient = UserModel.query.filter_by(email=email.data,role="patient").first()
        if not patient:
            raise ValidationError("Patient with this email doesn't exist.")


class PatientResetPasswordForm(FlaskForm):
    password = PasswordField("Password",validators=[DataRequired(),Length(min=2, max=20)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Reset Password")