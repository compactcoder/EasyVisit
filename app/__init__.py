import os
from flask import Flask,request
# from flask_login import current_user
from app.extentions import db, bcrypt, login_manager, mail
# from EasyVisit.config import Config


def create_app(db_url = None):
    app = Flask(__name__)
    # app.config.from_object(Config)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SECRET_KEY"] = 'e334b7f893a7d17a9f6a80d25e06bda1'
    app.config["SECURITY_PASSWORD_SALT"] = 'my_precious_two'

    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True


    app.config['MAIL_USERNAME'] = "xyz@gmail.com"
    app.config['MAIL_PASSWORD'] = "xnvs nqdv pqeg xllb"
    app.config['MAIL_DEFAULT_SENDER'] = 'from@example.com'

    # Registering extentions
    db.init_app(app)

    with app.app_context():
        from app.models import UserModel,PatientModel,DoctorModel
        db.create_all()
 
    bcrypt.init_app(app)

    login_manager.init_app(app)

    mail.init_app(app)


    # with app.app_context():
    #     # Import models here to avoid circular imports
    #     from app.models import PatientModel, PatientInformationModel
         
    #     # Create tables
    #     db.create_all()
    #     print("Database -tables created")

    # Registering blueprints
    from app.patient import bp as patient_bp
    app.register_blueprint(patient_bp,url_prefix='/patient')

    from app.doctor import bp as doctor_bp
    app.register_blueprint(doctor_bp,url_prefix='/doctor')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

