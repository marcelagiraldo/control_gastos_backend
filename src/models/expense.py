from datetime import datetime
from src.database import db,ma
from sqlalchemy.orm import validates
import re

class Expense(db.Model):
    id     = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    date_hour       = db.Column(db.DateTime)
    value      = db.Column(db.Float,nullable=False)
    cumulative = db.Column(db.Float, nulllable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    user_id    =db.Column(db.String(10),db.ForeignKey('user.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False)

    def __init__(self, **fields):
        super().__init__(**fields)

    def __repr__(self) -> str:
        return f"User >>> {self.name}"

class ExpenseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields = ()
        model = Expense
        include_fk = True

revenue_schema = ExpenseSchema()
revenues_schema = ExpenseSchema(many=True)
