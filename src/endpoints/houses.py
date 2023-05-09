from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
from src.database import db
import werkzeug

from src.models.house import House, house_schema, houses_schema

houses = Blueprint("houses",__name__,url_prefix="/api/v1")

@houses.get("/houses")
def read_all():
 houses = House.query.order_by(House.address).all()
 return {"data": houses_schema.dump(houses)}, HTTPStatus.OK

@houses.get("/houses/<int:registration>")
def read_one(registration):
    house = House.query.filter_by(registration=registration).first()

    if(not house):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    return {"data":house_schema.dump(house)},HTTPStatus.OK


@houses.post("/users/<int:user_id>/houses")
def create(user_id):
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Post body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST

    house = House(address = request.get_json().get("address",None),
                type = request.get_json().get("type",None),
                flour_count = request.get_json().get("flour_count",None),
                user_id = user_id)

    try:
        db.session.add(house)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":house_schema.dump(house)},HTTPStatus.CREATED

#@houses.patch('/<int:id>')
@houses.put('/users/<int:user_id>/houses/<int:registration>')
def update(registration,user_id):
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Put body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST

    house = House.query.filter_by(registration=registration).first()

    if (not house):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    house.address = request.get_json().get("address",house.address)
    house.type = request.get_json().get("type",house.type)
    house.flour_count = request.get_json().get("flour_count",house.flour_count)
    
    if (user_id != house.user_id):
        house.user_id = user_id

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":house_schema.dump(house)},HTTPStatus.OK

@houses.delete("/houses/<int:registration>")
def delete(registration):
    house = House.query.filter_by(registration=registration).first()
    if (not house):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    try:
        db.session.delete(house)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":house_schema.dump(house)},HTTPStatus.NO_CONTENT
