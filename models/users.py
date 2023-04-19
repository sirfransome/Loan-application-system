from db import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    mobile_number = db.Column(db.String(15), unique=True, nullable=False)


    def __init__(self, first_name, last_name, mobile_number, email, password):
        
        self.first_name = first_name
        self.last_name = last_name
        self.mobile_number = mobile_number
        self.email = email
        self.password = password

    def get_id(self):
        return str(self.user_id)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_userid(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
    
    def add_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
    
        