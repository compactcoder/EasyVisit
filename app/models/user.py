import datetime
from flask import current_app
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_login import UserMixin
from app.extentions import db,bcrypt, login_manager


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


class UserModel(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10),nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    token_sent_on = db.Column(db.DateTime, nullable=True)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    patient = db.relationship('PatientModel', backref='user', uselist=False, cascade="all, delete-orphan")
    doctor = db.relationship('DoctorModel', backref='user', uselist=False, cascade="all, delete-orphan")

    def __init__(self, full_name, email, password, role):
        self.full_name = full_name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        self.role = role
        if role == "patient":
            self.image_file = "patient-default.png"
        elif role == "doctor": 
            self.image_file = "doctor-default.png"
        else:
            self.image_file = "default.png"
        self.registered_on = datetime.datetime.now()

    def change_password(self,new_password):
        self.password = bcrypt.generate_password_hash(new_password).decode("utf-8")

    def is_confirmed(self):
        self.confirmed = True
        self.confirmed_on = datetime.datetime.now()

    # def token_sent(self):
    #     self.token_sent_on = datetime.datetime.now()
    # def generate_token(self):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     return s.dumps({'user_id': self.id, 'email': self.email},
    #                    salt=current_app.config['SECURITY_PASSWORD_SALT'])
    
    # @staticmethod
    # def verify_token(token,expiration=1800):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         token_response = s.loads(token,
    #                           salt=current_app.config['SECURITY_PASSWORD_SALT'],
    #                           max_age=expiration)
    #         print(token_response)
    #         user_id = token_response["user_id"]
    #     except:
    #         return None
    #     return UserModel.query.get(user_id)

    def __repr__(self) -> str:
        return f"User( '{self.id}', '{self.full_name}', '{self.email}, '{self.role}', '{self.image_file}', '{self.registered_on}', '{self.confirmed}')"




    # __mapper_args__ = {
    #     'polymorphic_identity': 'user',
    #     'polymorphic_on': role
    # }