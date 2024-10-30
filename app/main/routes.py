from flask import Flask,redirect,render_template,url_for,flash
from flask_login import current_user
from app.main import bp
from app.models import PatientModel, DoctorModel

@bp.route('/',methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        print(current_user)
        if isinstance(current_user, DoctorModel):
            print("its doc")
            return redirect(url_for('doctor.dashboard'))
        elif isinstance(current_user, PatientModel):
            print("its patient")
            return redirect(url_for('patient.dashboard')) 
    return redirect(url_for("patient.login"))

@bp.route('/about-us')
def about_us():
    return render_template('main/about-us.html', title = 'About Us')

@bp.route('/contact-us')
def contact_us():
    return render_template('main/contact-us.html', title = 'Contact Us')

@bp.route('/doctor-directory')
def doctor_directory():
    return render_template('main/doctor-directory.html', title = 'Doctor Directory')