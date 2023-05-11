from datetime import datetime
from src.database import db,ma
from sqlalchemy.orm import validates
import re

class Expense(db.Model):
    id     = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    date_hour  = db.Column(db.DateTime)
    value      = db.Column(db.Double,nullable=False)
    cumulative = db.Column(db.Double)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    user_document    =db.Column(db.String(10),db.ForeignKey('user.document',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False)

    def __init__(self, **fields):
        super().__init__(**fields)

    def __repr__(self) -> str:
        return f"Expense >>> {self.id}"

class ExpenseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields = ()
        model = Expense
        include_fk = True

expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)
