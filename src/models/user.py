from datetime import datetime
from src.database import db,ma
from werkzeug.security import generate_password_hash,check_password_hash
from src.models.expense import Expense
from src.models.revenue import Revenue
#from sqlalchemy.orm import validates
import re

class User(db.Model):
    document  = db.Column(db.String(10),primary_key=True)
    document_type = db.Column(db.String(80),nullable=False)
    name       = db.Column(db.String(80),nullable=False)
    lastname   = db.Column(db.String(80),nullable=False)
    password   = db.Column(db.String(128),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    expenses = db.relationship('Expense', backref="owner_expense")
    revenues = db.relationship('Revenue', backref="owner_revenue")

    def __init__(self, **fields):
        super().__init__(**fields)

    def __repr__(self) -> str:
        return f"User >>> {self.name}"

    def __setattr__(self, name, value):
        if(name == "password"):
            value = User.hash_password(value)
        super(User,self).__setattr__(name, value)

    @staticmethod
    def hash_password(password):
        '''  if not password:
            raise AssertionError('Password not provided')

        if not re.match('\d.*[A-Z]|[A-Z].*\d', password):
            raise AssertionError('Password must contain 1 capital letter and 1 number')

        if len(password) < 7 or len(password) > 50:
            raise AssertionError('Password must be between 7 and 50 characters') '''
        return generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

    ''' @validates('id')
    def validate_id(self,value):
        if not value:
            raise AssertionError('No id provided')
        if not value.isalnum():
            raise AssertionError('Id value must be alphanumeric')
        if len(value) < 3 or len(value) > 10:
            raise AssertionError('Id must be between 3 and 10 characters')
        if User.query.filter(User.id == value).first():
            raise AssertionError('Id is already in use')

        return value

    @validates('name')
    def validate_name(self, value):
        if not value:
            raise AssertionError('No name provided')
        if not value.isalnum():
            raise AssertionError('Name value must be alphanumeric')
        if len(value) < 5 or len(value) > 80:
            raise AssertionError('Name must be between 5 and 80 characters')

        return value

    @validates('email')
    def validate_email(self, key, value):
        if not value:
            raise AssertionError('No email provided')
        if not re.match("[^@]+@[^@]+\.[^@]+", value):
            raise AssertionError('Provided email is not an email address')
        if User.query.filter(User.email == value).first():
            raise AssertionError('Email is already in use')
        return value '''

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields = ()
        model = User
        include_fk = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)


