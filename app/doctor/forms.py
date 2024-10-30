import string
from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, MultipleFileField, SelectMultipleField, StringField,PasswordField,SubmitField,IntegerField,SelectField, TextAreaField, TimeField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired,Length, Email ,EqualTo,Regexp, ValidationError,NumberRange,InputRequired

from wtforms.widgets import CheckboxInput, ListWidget
from flask_login import current_user
from app.models import DoctorModel,UserModel

from app.doctor.utils import doctor_specialties, indian_languages, indian_cities, week_days


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class DoctorLoginForm(FlaskForm):
    email = StringField("Email",validators =[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=2, max=20)])
    submit = SubmitField("Login")

class DoctorRegistrationForm(FlaskForm):
    full_name = StringField("Full Name",
                           validators=[DataRequired(), Length(min=2, max=40)])
    # phone_number = StringField('Phone Number', validators=[DataRequired(),Length(min=10, max=10, message='Mobile number must be 10 digits long'),
    #                                                         Regexp(r'^[6789]\d{9}$', message='Invalid mobile number format')])
    email = StringField("Email",validators =[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=2, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField("Sign Up")

    def validate_email(self,email):
        doctor = UserModel.query.filter_by(email=email.data,role="doctor").first()
        if doctor:
            raise ValidationError("Doctor with this email is already registered.")



## Patient Profile Update Form
class DoctorProfileUpdateForm(FlaskForm):
    #mandatory fields
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    phone_no = StringField('Phone Number', validators=[DataRequired(),Length(min=10, max=10, message='Mobile number must be 10 digits long'),Regexp(r'^[6789]\d{9}$', message='Invalid mobile number format')])

    speciality = SelectField("Speciality",choices=[(i,i) for i in doctor_specialties],validators=[DataRequired()])

    qualification = StringField("Qualification",validators=[DataRequired(), Length(min=2, max=80)])
    experience = IntegerField("Experience")
    languages = SelectMultipleField("Languages (press 'ctrl' for selecting multiple languages)",choices=[(i,i) for i in indian_languages])
    
    address = TextAreaField("Adress",validators=[DataRequired(),Length(max=200)])
    city = SelectField("City",choices=[(i,i) for i in indian_cities],validators=[DataRequired()])

    submit = SubmitField("Update Profile")


class DoctorGetResetLinkForm(FlaskForm):
    email = StringField("Email",validators =[DataRequired(), Email()])
    submit = SubmitField("Get Password Reset Link")
    
    # Emaiil validation in database
    def validate_email(self,email):
        doctor = UserModel.query.filter_by(email=email.data,role="doctor").first()
        if not doctor:
            raise ValidationError("Doctor with this email doesn't exist.")


class DoctorResetPasswordForm(FlaskForm):
    password = PasswordField("Password",validators=[DataRequired(),Length(min=2, max=20)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Reset Password")


## Patient Profile Update Form
    
# class SelectMultipleFieldWithCheckboxes(SelectMultipleField):
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()




    # picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    # phone_no = StringField('Phone Number', validators=[DataRequired(),Length(min=10, max=10, message='Mobile number must be 10 digits long'),Regexp(r'^[6789]\d{9}$', message='Invalid mobile number format')])

    # speciality = SelectField("Speciality",choices=[(i.lower(),i) for i in doctor_specialties],validators=[DataRequired()])
    # qualification = StringField("Qualification",validators=[DataRequired(), Length(min=2, max=50)])
    # languages = MultiCheckboxField("Languages (press 'ctrl' for selecting multiple languages)",choices=[(i.lower(),i) for i in indian_languages])
    # experience = IntegerField("Experience")
    # address = TextAreaField("Adress",validators=[DataRequired(),Length(max=200)])
    # city = SelectField("City",choices=[(i.lower(),i) for i in indian_cities],validators=[DataRequired()])

class DoctorTestForm(FlaskForm):
        # Define choices for time selection dropdowns with 30-minute intervals
    time_choices_30_minutes = [(f'{hour:02}:{minute:02}', f'{hour:02}:{minute:02}') for hour in range(0, 24) for minute in range(0, 60, 30)]

    # Dropdown for start time selection with 30-minute intervals
    start_time = SelectField('Start Time', choices=time_choices_30_minutes, validators=[InputRequired()])

    # Dropdown for end time selection with 30-minute intervals
    end_time = SelectField('End Time', choices=time_choices_30_minutes, validators=[InputRequired()])
    # start_time = TimeField('Start Time', validators=[InputRequired()])
    # end_time = TimeField('End Time', validators=[InputRequired()])

    duration_choices = [(15, '15'), (30, '30'), (45, '45'), (60, '60')]
    duration = SelectField('Consultation Duration (in minutes)', choices=duration_choices, coerce=int, validators=[InputRequired()])
    # duration = IntegerField('Duration (in minutes)', validators=[InputRequired(), NumberRange(min=1)])
    days = MultiCheckboxField('Select Days', choices=[(i[:3],i) for i in week_days])
    submit = SubmitField("Update Profile")