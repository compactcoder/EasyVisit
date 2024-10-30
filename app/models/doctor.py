from app.extentions import db

from flask_sqlalchemy import SQLAlchemy
import json
from app.models import UserModel


class DoctorModel(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    # image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    # id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    phone_no = db.Column(db.String(15), nullable=False)
    speciality = db.Column(db.String(100),nullable=False)
    qualification = db.Column(db.String(100),nullable=False)
    experience = db.Column(db.Integer,nullable=False)
    languages = db.Column(db.String)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    
    def __init__(self,user_id,phone_no,speciality,qualification,experience,languages,address,city):
        self.user_id = user_id
        self.phone_no = phone_no
        self.speciality = speciality
        self.qualification = qualification
        self.experience = experience
        self.languages = json.dumps(languages)
        self.address = address
        self.city = city


    def __repr__(self):
        return f"<Doctor {self.name}>"

    def set_languages(self, languages):
        self.languages = json.dumps(languages)

    def get_languages(self):
        return json.loads(self.languages) if self.languages else []

    # __mapper_args__ = {
    #     'polymorphic_identity': 'doctor'
    # }