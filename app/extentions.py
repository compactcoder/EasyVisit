from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


from flask_login import LoginManager

login_manager = LoginManager()


from flask_mail import Mail

mail = Mail()

"""
How to create database and their tables?

first import these things.

from app import create_app
from app.extentions import db
from app.models import PatientModel, UserModel
app = create_app()

app.app_context().push()

db.create_all()
user1 = UserModel(fullname="test patient",email="test@easyvisit.com",password="1234",role="patient")
patient1 = PatientModel(user_id=user1.id,phoneno="9898767654",age="18",gender="male",address="surat") 

user1 = PatientModel(fullname="bhavik",email="hihello@gmail.com",password="nothing")
db.session.add(user1) 
db.session.commit()

user1info = PatientInformationModel(phoneno="1231231234",age="24",gender="male",address="sec2b,gandhinagae", height="176",weight="80",patient_id="1")
db.session.add(user1info)                                                                     
db.session.commit()

# Query a specific patient by ID
patient = PatientModel.query.get(1)

# Access patient information using the one-to-one relationship
print(patient.information.phoneno)
print(patient.information.age)

# ...


"""