from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
from src.database import db
import werkzeug

from src.models.user import User, user_schema, users_schema
from flask_jwt_extended import jwt_required


users = Blueprint("users",__name__,url_prefix="/api/v1/users")

@jwt_required()
@users.get("/current")
def read_current():
    user = User.query.filter_by(id=get_jwt_identity()).first()
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data": user_schema.dump(user)}, HTTPStatus.OK
@users.get("/")
def read_all():
 users = User.query.order_by(User.name).all()
 return {"data": users_schema.dump(users)}, HTTPStatus.OK

@users.get("/<int:id>")
def read_one(id):
    user = User.query.filter_by(id=id).first()

    if(not user):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    return {"data":user_schema.dump(user)},HTTPStatus.OK


@users.post("/")
def create():
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Posr body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST

    user = User(id = request.get_json().get("id",None),
                name = request.get_json().get("name",None),
                email = request.get_json().get("email",None),
                password = request.get_json().get("password",None))

    try:
        db.session.add(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":user_schema.dump(user)},HTTPStatus.CREATED

@users.patch('/<int:id>')
@users.put('/<int:id>')
def update(id):
    post_data=None

    try:
        post_data=request.get_json()

    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Post body JSON data not found",
                "message":str(e)}, HTTPStatus.BAD_REQUEST

    user=User.query.filter_by(id=id).first()

    if(not user):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    user.name=request.get_json().get("name", user.name)
    user.email=request.get_json().get("email", user.email)
    user.password=request.get_json().get("password", user.password)

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message":str(e)}, HTTPStatus.BAD_REQUEST

    return {"data":user_schema.dump(user)}, HTTPStatus.OK

@users.delete("/<int:id>")
def delete(id):
    user = User.query.filter_by(id=id).first()
    if (not user):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    try:
        db.session.delete(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":user_schema.dump(user)},HTTPStatus.NO_CONTENT
#Proveedores de un producto
''' @users.get("/<int:id_user>/providers")
def read_providers(id):
    pass '''
