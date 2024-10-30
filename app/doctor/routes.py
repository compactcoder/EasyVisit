
import datetime
import imp
import json
from pydoc import doc
from flask import Flask,redirect,render_template,url_for,flash,request
from flask_login import login_user,logout_user,login_required, current_user

from app.doctor.forms import DoctorLoginForm, DoctorRegistrationForm,DoctorProfileUpdateForm,DoctorGetResetLinkForm,DoctorResetPasswordForm,DoctorTestForm
from app.doctor import bp
from app.utils import save_picture

from app.extentions import db, bcrypt
from app.models import UserModel, DoctorModel
from app.utils import generate_confirmation_token, confirm_token,send_email, email_verified


@bp.route('/',methods=["GET", "POST"])
def index():
    if current_user.is_authenticated and current_user.role == "doctor":
            return redirect(url_for('doctor.dashboard')) 
    return redirect(url_for("doctor.login"))

@bp.route('/register',methods=["GET","POST"])
def register():

    if current_user.is_authenticated and current_user.role == "doctor":
        return redirect(url_for('doctor.dashboard'))
    
    form = DoctorRegistrationForm()

    if form.validate_on_submit():
        # print(form.data, "validated on front end")
        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = UserModel(full_name=form.full_name.data, email=form.email.data,password=form.password.data,role="doctor")
        db.session.add(user)
        db.session.commit()
 
        flash(f'Account created for {form.email.data}! You can login now.', 'green')
        return redirect(url_for('doctor.login'))
    
    return render_template('doctor/registration.html' , title = 'Doctor Register',form=form)

@bp.route('/login',methods=["GET", "POST"])
@email_verified
def login():
    # print(current_user)
    if current_user.is_authenticated and current_user.role == "doctor":
        return redirect(url_for('doctor.dashboard'))
    
    form = DoctorLoginForm()
    if form.validate_on_submit():
        doctor = UserModel.query.filter_by(email=form.email.data).first()
        if doctor and doctor.role == "doctor" and bcrypt.check_password_hash(doctor.password,form.password.data):
            login_user(doctor)
            return redirect(url_for("doctor.dashboard"))
        else:
            flash('Invalid Password. Please verify your password and try again!', 'red')
    return render_template('doctor/login.html', title = 'Doctor Login', form = form)

@bp.route('/verify')
@login_required
def verify():
    # print(type(current_user.token_sent_on))
    if current_user.confirmed:
        flash(f'Your email is already verified.', 'green')
        return redirect(url_for('doctor.dashboard'))
    
    elif not current_user.token_sent_on or datetime.datetime.now() - current_user.token_sent_on  > datetime.timedelta(seconds=3600):
        token = generate_confirmation_token(current_user.email)
        confirm_url = url_for('doctor.confirm', token=token, _external=True)
        html = render_template('mail-layout.html',type="email_verification", url=confirm_url)
        subject = "Please confirm your email"
        send_email(current_user.email, subject, html)
        current_user.token_sent_on = datetime.datetime.now()
        db.session.commit()
        flash(f'Your email is not verified. Please verify your email address.', 'red')
        return render_template('doctor/verify.html', title = 'doctor Verification')

    flash(f'Email verification link is already been sent. Please follow the link to verify your email.', 'yellow')
    return render_template('doctor/verify.html', title = 'doctor Verification')

@bp.route('/confirm/<token>',methods=["GET","POST"])
@login_required
def confirm(token):
    try:
        email = confirm_token(token)
        user = UserModel.query.filter_by(email=email).first_or_404()
        # print(email)
    except:
        flash('The confirmation link is invalid or has expired.', 'red')
        return redirect(url_for('doctor.verify'))
    
    if user.confirmed:
        flash('Account already confirmed.', 'green')
    else:
        user.is_confirmed()
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'green')
    return redirect(url_for('doctor.dashboard'))

@bp.route('/reset', methods=["GET", "POST"])
def get_reset_link():

    form = DoctorGetResetLinkForm()
    if form.validate_on_submit():
        email = form.email.data
        token = generate_confirmation_token(email)
        confirm_url = url_for('doctor.reset_password', token=token, _external=True)
        html = render_template('mail-layout.html',type="password_reset", url=confirm_url)
        subject = "Password Reset"
        send_email(email, subject, html)
        flash('Password reset link haas been shared to registerd email. Please follow the link to reset your password.', 'green')
        # doctor = UserModel.query.filter_by(email=form.email.data).first()
        return redirect(url_for('doctor.login')) 
    
    return render_template('doctor/resetlink.html', title = 'Doctor Reset',form = form)

@bp.route('/resetpassword/<token>',methods=["GET","POST"])
def reset_password(token):
    form = DoctorResetPasswordForm()
    try:
        email = confirm_token(token)
        user = UserModel.query.filter_by(email=email).first_or_404()
    except:
        flash('Invalid Operation', 'yellow')
        return redirect(url_for('doctor.login'))
    
    if form.validate_on_submit():
        user.change_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'green')
        return redirect(url_for('doctor.login'))
    return render_template('doctor/resetpassword.html', tilte= 'Doctor password Reset', form =form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("doctor.login"))

@bp.route('/dashboard')
@login_required
@email_verified
def dashboard():
    doctorprofile = DoctorModel.query.filter_by(user_id=current_user.id).first()
    if not doctorprofile:
        flash(f'Welcome Dr. {current_user.full_name}! Please complete your profile first.', 'green')
        return redirect(url_for("doctor.profile"))
    flash(f'Welcome Dr. {current_user.full_name}!', 'green')

    return render_template('doctor/dashboard.html' , title = 'Dashboard')

@bp.route('/account')
@login_required
@email_verified
def account():
    if current_user.is_authenticated and current_user.role == "doctor":
        return render_template('doctor/account.html' , title = 'Account')
    return redirect(url_for("doctor.login"))

@bp.route('/profile',methods=["GET","POST"])
@login_required
@email_verified
def profile():
    if current_user.is_authenticated and current_user.role == "doctor":
        form = DoctorProfileUpdateForm()

        doctor_profile = DoctorModel.query.filter_by(user_id=current_user.id).first()

        if doctor_profile:
            print("in doc profile")
        # If Doctor's profile already exists and user loads the profile page, below condition will show the profile.
            if request.method == "GET":
                print("in get")
                form.phone_no.data = doctor_profile.phone_no
                form.speciality.data = doctor_profile.speciality
                form.qualification.data = doctor_profile.qualification
                form.experience.data = doctor_profile.experience
                form.languages.data = doctor_profile.get_languages()
                form.address.data = doctor_profile.address
                form.city.data = doctor_profile.city

            # If Doctor's profile already exists and user updates the profile page, below condition will update the Doctor's profile.
            elif form.validate_on_submit():
                if form.picture.data:
                    # print("in second loop")
                    picture_file = save_picture(form.picture.data)
                    current_user.image_file = picture_file
                # print("in elif")
                # print(form.qualification.data)
                doctor_profile.phone_no = form.phone_no.data
                doctor_profile.speciality = form.speciality.data
                doctor_profile.qualification = form.qualification.data
                doctor_profile.experience = form.experience.data
                doctor_profile.set_languages(form.languages.data)
                doctor_profile.address = form.address.data
                doctor_profile.city = form.city.data
                db.session.commit()
                flash(f'Profile has been updated for {current_user.full_name}.', 'green')
            
            return render_template('doctor/profile.html' , form= form, title = 'Profile')

        # If Doctor's profile doesn't exist and user fills the profile page, below condition will create the Doctor's profile.
        if form.validate_on_submit():
            # print("in lastprofile")
            if form.picture.data:
                current_user.image_file = save_picture(form.picture.data)
    
            print(form.qualification.data)
            new_doctor_profile = DoctorModel(user_id=current_user.id, phone_no=form.phone_no.data, speciality=form.speciality.data, qualification=form.qualification.data,experience=form.experience.data,languages = form.languages.data, address = form.address.data, city = form.city.data )

            db.session.add(new_doctor_profile)
            db.session.commit()

            flash(f'Profile has been updated for {current_user.full_name}.', 'green')
            return redirect(url_for('doctor.dashboard'))
        
        return render_template('doctor/profile.html' , form= form , title = 'Profile')
    else:
        return redirect(url_for("patient.login"))
    
@bp.route('/test',methods=["GET","POST"])
@login_required
@email_verified
def test():
    form = DoctorTestForm()
    if form.validate_on_submit():
        selected_days = json.dumps(form.days.data)
        start_time =  form.start_time.data
        
        # Print form data to terminal
        print("Selected Days:", json.loads(selected_days))
        print("start_time:", start_time)
        # Further processing or database insertion can be done here
        
        # return f'Selected Days: {", ".join(selected_days)}'
    return render_template('doctor/test.html' , form= form , title = 'test')
