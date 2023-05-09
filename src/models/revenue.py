from datetime import datetime
from src.database import db,ma
from sqlalchemy.orm import validates
import re

class Revenue(db.Model):
    id     = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    date_hour       = db.Column(db.DateTime)
    value      = db.Column(db.Float,nullable=False)
    cumulative = db.Column(db.Date, nulllable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    user_id    =db.Column(db.String(10),db.ForeignKey('user.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False)

    def __init__(self, **fields):
        super().__init__(**fields)

    def __repr__(self) -> str:
        return f"User >>> {self.name}"

class RevenueSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields = ()
        model = Revenue
        include_fk = True

revenue_schema = RevenueSchema()
revenues_schema = RevenueSchema(many=True)
