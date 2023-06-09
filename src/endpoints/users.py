from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
from src.database import db
import werkzeug
from src.models.user import User, user_schema, users_schema
from flask_jwt_extended import jwt_required,get_jwt_identity
from datetime import datetime
from src.models.expense import Expense,expenses_schema
from src.models.revenue import Revenue,revenues_schema

users = Blueprint("users",__name__,url_prefix="/api/v1/users")

''' lista al usuario autenticado '''
@users.get("/")
@jwt_required()
def read_user():
    user = User.query.filter_by(document=get_jwt_identity()['document']).one_or_none()

    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data": user_schema.dump(user)}, HTTPStatus.OK

''' listar todos los usuarios de la base de datos '''
@users.get("/todos")
def read_all():
    users = User.query.order_by(User.name).all()
    return {"data": users_schema.dump(users)}, HTTPStatus.OK

''' crear un usuario '''
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

''' actualizar un usuario '''
@users.put('/')
@jwt_required()
def update_user():

    user=User.query.filter_by(document=get_jwt_identity()['document']).one_or_none()

    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

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

''' eliminar el usuario '''
@users.delete("/<int:document>")
def delete_user(document):
    user = User.query.filter_by(document=document).first()
    if (not user):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND 
    
    try:
        db.session.delete(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":user_schema.dump(user)},HTTPStatus.NO_CONTENT

''' obtener el balance del usuario autenticado '''
@users.get("/balance")
@jwt_required()
def Balance():
    user=read_user()[0]['data']
    userDocument=user['document']
    expense = Expense.query.filter(Expense.user_document == userDocument).all()
    revenue = Revenue.query.filter(Revenue.user_document == userDocument).all()
    total_expense = sum(exp.value for exp in expense)
    total_revenue = sum(rev.value for rev in revenue)

    balance = total_revenue - total_expense

    return {"balance": balance}
