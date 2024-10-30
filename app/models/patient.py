from app.extentions import db
from app.models import UserModel

class PatientModel(db.Model):
    __tablename__ = "patients"
    # id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)

    # Mandatory fields
    phone_no = db.Column(db.String(15), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    
    # Optional fields
    height = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)

    # __mapper_args__ = {
    #     'polymorphic_identity': 'patient'
    # }

    
    # # Define foreign key
    # patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), unique=True, nullable=False)

    # # Define back-reference to PatientModel
    # patient = db.relationship('PatientModel', back_populates='information')

  





# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin

# class PatientModel(db.Model, UserMixin):
#     __tablename__ = "patients"
#     id = db.Column(db.Integer, primary_key=True)
#     fullname = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)

#     # Define one-to-one relationship with PatientInformationModel
#     information = db.relationship('PatientInformationModel', back_populates='patient', uselist=False, cascade='all, delete-orphan')

    # def __repr__(self) -> str:
    #     return f"User( '{self.fullname}','{self.email}','{self.information.age},'{self.information.gender}')"
    

 