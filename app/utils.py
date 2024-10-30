from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def email_verified(view_func):
    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        
        if current_user.is_authenticated and current_user.role == "patient" :
            if not current_user.confirmed:
                return redirect(url_for('patient.verify'))
            
        elif current_user.is_authenticated and current_user.role == "doctor" :
            if not current_user.confirmed:
                return redirect(url_for('doctor.verify'))
        
        return view_func(*args, **kwargs)
    
    return decorated_function




from itsdangerous import URLSafeTimedSerializer

from flask import current_app
from app.extentions import mail
from flask_mail import Message


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


import secrets
from PIL import Image
from flask import current_app

import os

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
