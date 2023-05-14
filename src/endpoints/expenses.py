from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
from src.database import db
import werkzeug
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from src.models.expense import Expense, expense_schema, expenses_schema
from src.endpoints.users import read_user
from flask_jwt_extended import jwt_required

expenses = Blueprint("expenses",__name__,url_prefix="/api/v1/expenses")

''' Listar todos los egregos perdenecientes al usuario que se encuentra autenticado '''
@expenses.get("/")
def read_expenses():
    user = read_user()[0]['data']
    print(f'datos usuario: {user}')
    userDocument = user['document']

    expense = Expense.query.filter_by(user_document=userDocument).all()

    if(not expense):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    return {"data": expenses_schema.dump(expense)}, HTTPStatus.OK

@expenses.get("/todos")

def read_all():

    expense = Expense.query.filter(Expense.id).all()

    if(not expense):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    return {"data": expenses_schema.dump(expense)}, HTTPStatus.OK

''' Consulta sobre fechas '''
@expenses.get("/consulta")
def consulta_fecha():
    user = read_user()[0]['data']
    print(f'datos usuario: {user}')
    userDocument = user['document']

    inicio = datetime.strptime(request.args.get('inicio'), '%Y-%m-%d')
    fin = datetime.strptime(request.args.get('fin'), '%Y-%m-%d')

    print(f'Los datos de consulta son: {userDocument}, {inicio}, {fin}')

    revenue = Expense.query.order_by(Expense.id).filter(Expense.user_document==userDocument,Expense.date_hour >= inicio, Expense.date_hour < fin + timedelta(days=1)).all()

    return {"data": expenses.dump(revenue)}, HTTPStatus.OK

''' Listar un ingreso perdeneciente al usuario que se encuentra autenticado '''
@expenses.get("/<int:id>")
def read_expense(id):
    expense = Expense.query.filter_by(id=id).first()

    if(not expense):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    return {"data":expense_schema.dump(expense)},HTTPStatus.OK

''' Crear un ingreso perdeneciente al usuario que se encuentra autenticado '''
@expenses.post("/")
def create():
    post_data = None
    user = read_user()[0]['data']
    userDocument = user['document']
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Post body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST

    date_hour = Expense.parse_date_hour(request.get_json().get("date_hour",None))

    expense = Expense(
                date_hour = date_hour,
                value = request.get_json().get("value",None),
                cumulative = request.get_json().get("cumulative",None),
                user_document = userDocument)

    try:
        db.session.add(expense)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":expense_schema.dump(expense)},HTTPStatus.CREATED

''' Actualizar un ingreso perdeneciente al usuario que se encuentra autenticado'''
@expenses.put('/<int:id>')
def update_revenue(id):
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Put body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST

    expense = Expense.query.filter_by(id=id).first()

    if (not expense):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    expense.date_hour = Expense.parse_date_hour(request.get_json().get("date_hour",expense.date_hour))
    expense.value = request.get_json().get("value",expense.value)
    expense.cumulative = request.get_json().get("cumulative",expense.cumulative)

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":expense_schema.dump(expense)},HTTPStatus.OK

@expenses.delete("/<int:id>")
def delete(id):
    expense = Expense.query.filter_by(id=id).first()
    if (not expense):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    try:
        db.session.delete(expense)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":expense_schema.dump(expense)},HTTPStatus.NO_CONTENT
