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

@users.get("/")
@jwt_required()
def read_user():
    user = User.query.filter_by(document=get_jwt_identity()['document']).one_or_none()

    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data": user_schema.dump(user)}, HTTPStatus.OK

@users.get("/users")
def read_all():
    users = User.query.order_by(User.name).all()
    return {"data": users_schema.dump(users)}, HTTPStatus.OK
'''
@users.get("")
def readUser():
    user = User.query.filter_by(document=document).first()
    if(not user):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data":user_schema.dump(user)},HTTPStatus.OK '''

@users.get("/expenses") # api/v1/expenses?inicio=2023-05-09&fin=2023-05-10
@jwt_required()
def consulta_fecha_egresos():
    inicio = datetime.strptime(request.args.get('inicio'), '%Y-%m-%d')
    fin = datetime.strptime(request.args.get('fin'), '%Y-%m-%d')
    
    user = User.query.filter_by(document=get_jwt_identity()).first()
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    
    expense = Expense.query.order_by(Expense.id).filter(Expense.user_document == user.document, Expense.created_at >= inicio, Expense.created_at <= fin).all()

    return {"data": expenses_schema.dump(expense)}, HTTPStatus.OK

@users.get("/revenues") # api/v1/revenues?inicio=2023-05-09&fin=2023-05-10
@jwt_required()
def consulta_fecha_ingresos():
    inicio = datetime.strptime(request.args.get('inicio'), '%Y-%m-%d')
    fin = datetime.strptime(request.args.get('fin'), '%Y-%m-%d')
    
    user = User.query.filter_by(document=get_jwt_identity()).first()
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    
    revenue = Revenue.query.order_by(Revenue.id).filter(Revenue.user_document == user.document, Revenue.created_at >= inicio, Revenue.created_at <= fin).all()

    return {"data": revenues_schema.dump(revenue)}, HTTPStatus.OK

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

@users.delete("/")
@jwt_required()
def delete_user():
    user = User.query.filter_by(document=get_jwt_identity()['document']).one_or_none()
    if (not user):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND 
    
    try:
        db.session.delete(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":user_schema.dump(user)},HTTPStatus.NO_CONTENT

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
