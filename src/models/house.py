from datetime import datetime
from src.database import db,ma

class House(db.Model):
    registration = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    address      = db.Column(db.String(50),nullable=False,unique=True)
    type        = db.Column(db.Integer,nullable=False)
    flour_count = db.Column(db.Integer)
    created_at  = db.Column(db.DateTime, default=datetime.now())
    updated_at  = db.Column(db.DateTime, onupdate=datetime.now())
    user_id    =db.Column(db.String(10),db.ForeignKey('user.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False)

    def __init__(self, **fields):
        super().__init__(**fields)

    def __repr__(self) -> str:
        return f"User >>> {self.name}"

class HouseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields = ()
        model = House
        include_fk = True

house_schema = HouseSchema()
houses_schema = HouseSchema(many=True)
