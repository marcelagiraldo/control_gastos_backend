from datetime import datetime
from src.database import db,ma
from sqlalchemy.orm import validates
import re

class Product(db.Model):
    codigo     = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    name       = db.Column(db.String(50),unique=True,nullable=False)
    price      = db.Column(db.Float,nullable=False)
    expiration = db.Column(db.Date, nulllable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    user_id    =db.Column(db.String(10),db.ForeignKey('user.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False)

    products = db.relationship('Product',backref="owner")

    def __init__(self, **fields):
        super().__init__(**fields)

    def __repr__(self) -> str:
        return f"User >>> {self.name}"

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields = ()
        model = Product
        include_fk = True

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
