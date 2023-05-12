from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
from src.database import db
import werkzeug
from src.models.user import User, user_schema, users_schema
from flask_jwt_extended import jwt_required


users = Blueprint("users",__name__,url_prefix="/api/v1/users")

''' @jwt_required()
@users.get("/current")
def read_current():
    user = User.query.filter_by(id=get_jwt_identity()).first()
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data": user_schema.dump(user)}, HTTPStatus.OK '''

@users.get("/")
def read_all():
    users = User.query.order_by(User.name).all()
    return {"data": users_schema.dump(users)}, HTTPStatus.OK

@users.get("/<int:document>")
def read_one(document):
    user = User.query.filter_by(document=document).first()
    if(not user):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data":user_schema.dump(user)},HTTPStatus.OK


@users.get("/expenses")

@users.post("/")
def create():
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Posr body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST

    user = User(document = request.get_json().get("document",None),
                document_type = request.get_json().get("document_type",None),
                name = request.get_json().get("name",None),
                lastname = request.get_json().get("lastname",None),
                password = request.get_json().get("password",None))

    try:
        db.session.add(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":user_schema.dump(user)},HTTPStatus.CREATED

@users.patch('/<int:document>')
@users.put('/<int:document>')
def update(document):
    post_data=None

    try:
        post_data=request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Post body JSON data not found",
                "message":str(e)}, HTTPStatus.BAD_REQUEST

    user=User.query.filter_by(document=document).first()

    if(not user):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    user.document_type = request.get_json().get("document_type", user.document_type)
    user.name = request.get_json().get("name", user.name)
    user.lastname = request.get_json().get("lastname", user.lastname)
    user.password = request.get_json().get("password", user.password)

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values",
                "message":str(e)}, HTTPStatus.BAD_REQUEST

    return {"data":user_schema.dump(user)}, HTTPStatus.OK

@users.delete("/<int:document>")
def delete(document):
    user = User.query.filter_by(document=document).first()
    if (not user):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    try:
        db.session.delete(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":user_schema.dump(user)},HTTPStatus.NO_CONTENT

