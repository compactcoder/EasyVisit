
import datetime
from turtle import tilt, title
from flask import Flask,redirect,render_template,url_for,flash, request
from flask_login import login_user,logout_user,login_required,current_user
from app.utils import save_picture

from app.patient.forms import PatientLoginForm, PatientRegistrationForm, PatientProfileUpdateForm,PatientGetResetLinkForm,PatientResetPasswordForm

from app.patient import bp

from app.extentions import db, bcrypt
from app.models import UserModel, PatientModel
from app.utils import generate_confirmation_token, confirm_token,send_email, email_verified


@bp.route('/',methods=["GET", "POST"])
def index():
    if current_user.is_authenticated and current_user.role == "patient":
        return redirect(url_for('patient.dashboard')) 
    return redirect(url_for("patient.login"))

@bp.route('/register',methods=["GET","POST"])
def register():
    if current_user.is_authenticated and current_user.role == "patient":
        return redirect(url_for('patient.dashboard'))
    
    form = PatientRegistrationForm()

    if form.validate_on_submit():
        user = UserModel(full_name=form.full_name.data, email=form.email.data,password=form.password.data,role="patient")
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.email.data}! You can login now.', 'green')
        return redirect(url_for('patient.login'))
    
    return render_template('patient/registration.html' , title = 'Patient Register',form=form)

@bp.route('/login',methods=["GET", "POST"])
@email_verified
def login():
    if current_user.is_authenticated and current_user.role == "patient":
        return redirect(url_for('patient.dashboard'))
    
    form = PatientLoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user and user.role == "patient" and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            return redirect(url_for("patient.dashboard"))
        else:
            flash('Invalid Password. Please verify your password and try again!', 'red')
    return render_template('patient/login.html', title = 'Patient Login',form = form)

@bp.route('/verify')
@login_required
def verify():
    # print(type(current_user.token_sent_on))
    if current_user.confirmed:
        flash(f'Your email is already verified.', 'green')
        return redirect(url_for('patient.dashboard'))
    
    elif not current_user.token_sent_on or datetime.datetime.now() - current_user.token_sent_on  > datetime.timedelta(seconds=3600):
        token = generate_confirmation_token(current_user.email)
        confirm_url = url_for('patient.confirm', token=token, _external=True)
        html = render_template('mail-layout.html',type="email_verification", url=confirm_url)
        subject = "Please confirm your email"
        send_email(current_user.email, subject, html)
        current_user.token_sent_on = datetime.datetime.now()
        db.session.commit()
        flash(f'Your email is not verified. Please verify your email address.', 'red')
        return render_template('patient/verify.html', title = 'Patient Verification')

    flash(f'Email verification link is already been sent. Please follow the link to verify your email.', 'yellow')
    return render_template('patient/verify.html', title = 'Patient Verification')
    
@bp.route('/confirm/<token>',methods=["GET","POST"])
@login_required
def confirm(token):
    try:
        email = confirm_token(token)
        user = UserModel.query.filter_by(email=email).first_or_404()
        # print(email)
    except:
        flash('The confirmation link is invalid or has expired.', 'red')
        return redirect(url_for('patient.verify'))
    
    if user.confirmed:
        flash('Account already confirmed.', 'green')
    else:
        user.is_confirmed()
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'green')
    return redirect(url_for('patient.dashboard'))

@bp.route('/reset', methods=["GET", "POST"])
def get_reset_link():

    form = PatientGetResetLinkForm()
    if form.validate_on_submit():
        email = form.email.data
        token = generate_confirmation_token(email)
        confirm_url = url_for('patient.reset_password', token=token, _external=True)
        html = render_template('mail-layout.html',type="password_reset", url=confirm_url)
        subject = "Password Reset"
        send_email(email, subject, html)
        flash('Password reset link haas been shared to registerd email. Please follow the link to reset your password.', 'green')
        # patient = UserModel.query.filter_by(email=form.email.data).first()
        return redirect(url_for('patient.login')) 
    
    return render_template('patient/resetlink.html', title = 'Patient Reset',form = form)

@bp.route('/resetpassword/<token>',methods=["GET","POST"])
def reset_password(token):
    form = PatientResetPasswordForm()
    try:
        email = confirm_token(token)
        user = UserModel.query.filter_by(email=email).first_or_404()
    except:
        flash('Invalid Operation', 'yellow')
        return redirect(url_for('patient.login'))
    
    if form.validate_on_submit():
        user.change_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'green')
        return redirect(url_for('patient.login'))
    return render_template('patient/resetpassword.html', tilte= 'Patient password Reset', form =form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("patient.login"))

@bp.route('/dashboard')
@login_required
@email_verified
def dashboard():

    patientprofile = PatientModel.query.filter_by(user_id=current_user.id).first()

    if not patientprofile:
        flash(f'Welcome {current_user.full_name}! Please complete your profile first.', 'green')
        return redirect(url_for("patient.profile"))
    
    flash(f'Welcome {current_user.full_name}!', 'green')


    return render_template('patient/dashboard.html' , title = 'Dashboard')

@bp.route('/account')
@login_required
@email_verified
def account():
    if current_user.is_authenticated and current_user.role == "patient":
        return render_template('patient/account.html' , title = 'Account', user=f"{current_user.full_name}  ({current_user.email})")
    return redirect(url_for('patient.login')) 

@bp.route('/profile',methods=["GET", "POST"])
@login_required
@email_verified
def profile():
    if current_user.is_authenticated and current_user.role == "patient":
        form  =PatientProfileUpdateForm()

        patient_profile = PatientModel.query.filter_by(user_id=current_user.id).first()

        if patient_profile:

            if request.method == "GET":
                form.phone_no.data = patient_profile.phone_no
                form.age.data = patient_profile.age
                form.address.data = patient_profile.address
                form.gender.data = patient_profile.gender
                form.height.data = patient_profile.height
                form.weight.data = patient_profile.weight

            elif form.validate_on_submit():
                if form.picture.data:
                    picture_file = save_picture(form.picture.data)
                    current_user.image_file = picture_file

                patient_profile.phone_no = form.phone_no.data
                patient_profile.age = form.age.data
                patient_profile.address = form.address.data
                patient_profile.gender = form.gender.data
                patient_profile.height = form.height.data
                patient_profile.weight = form.weight.data 
                db.session.commit()
                flash(f'Profile has been updated for {current_user.full_name}.', 'green')
            
            return render_template('patient/profile.html' , form= form, title = 'Profile')

        if form.validate_on_submit():
            if form.picture.data:
                current_user.image_file = save_picture(form.picture.data)

            new_patient_profile = PatientModel(user_id=current_user.id, phone_no=form.phone_no.data, age=form.age.data, gender=form.gender.data,address=form.address.data, height=form.height.data, weight=form.weight.data)

            db.session.add(new_patient_profile)
            db.session.commit()

            flash(f'Profile has been updated for {current_user.email}.', 'green')
            return redirect(url_for('patient.dashboard'))
        
        return render_template('patient/profile.html', form= form, title = 'Profile')
    else:
        return redirect(url_for("doctor.login"))
    
