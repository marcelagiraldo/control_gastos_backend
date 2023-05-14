from datetime import datetime
from src.database import db,ma
from sqlalchemy.orm import validates
import re

class Revenue(db.Model):
    id     = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    date_hour  = db.Column(db.DateTime)
    value      = db.Column(db.Double,nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    user_document    =db.Column(db.String(10),db.ForeignKey('user.document',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False)

    def __init__(self, **fields):
        super().__init__(**fields)

    def __repr__(self) -> str:
        return f"Revenue >>> {self.id}"

    def parse_date_hour(date_hour_str):
        if (not date_hour_str):
            return None
        return datetime.strptime(date_hour_str, '%Y-%m-%d %H:%M')

class RevenueSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields = ()
        model = Revenue
        include_fk = True

revenue_schema = RevenueSchema()
revenues_schema = RevenueSchema(many=True)
