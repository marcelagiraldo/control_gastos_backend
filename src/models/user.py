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

    expenses = db.relationship('Expense', backref="owner")
    revenues = db.relationship('Revenue', backref="owner")

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
        return generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields = ()
        model = User
        include_fk = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)


