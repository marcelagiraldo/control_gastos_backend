from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
from src.database import db
import werkzeug
from datetime import datetime
from sqlalchemy.orm import Session
from src.models.expense import Expense, expense_schema, expenses_schema
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from src.models.user import User, user_schema, users_schema
from src.endpoints.users import read_one
import argparse

expenses = Blueprint("expenses",__name__,url_prefix="/api/v1")

@expenses.get("/expenses")
@jwt_required()
def read_all():
    
    user = read_one()
    ''' user = User.query.filter_by(id=get_jwt_identity()).first()
    if(not user):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND '''
    expense = Expense.query.order_by(Expense.id).filter(Expense.user_document == user.document).all()
    
    return {"data": expenses_schema.dump(expense)}, HTTPStatus.OK

@expenses.get("/expenses/<int:id>")
def read_one(id):
    expense = Expense.query.filter_by(id=id).first()

    if(not expense):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    return {"data":expense_schema.dump(expense)},HTTPStatus.OK


@expenses.post("/expenses")
@jwt_required()
def create():
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Post body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST
    user = read_one(self)
    
    #rawUser = User.query.filter_by(document=get_jwt_identity()).first()
    
    #if(not rawUser):
    #    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    #user = argparse.Namespace(**raw_user)
    #return {"data": user},HTTPStatus.OK
    date_hour = request.get_json().get("date_hour",None)
    date_hour_ = datetime.strptime(date_hour, '%Y-%m-%d %H:%M')

    expense = Expense(
                date_hour = date_hour_,
                value = request.get_json().get("value",None),
                cumulative = request.get_json().get("cumulative",None),
                user_document = user.document)

    try:
        db.session.add(expense)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":expense_schema.dump(expense)},HTTPStatus.CREATED

#@expenses.patch('/<int:id>')
@expenses.put('/users/<int:user_document>/expenses/<int:id>')
def update(id,user_document):
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Put body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST

    expense = Expense.query.filter_by(id=id).first()

    if (not expense):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    expense.date_hour = request.get_json().get("date_hour",expense.date_hour)
    expense.value = request.get_json().get("value",expense.value)
    expense.cumulative = request.get_json().get("cumulative",expense.cumulative)

    if (user_document != expense.user_document):
        expense.user_document = user_document

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":expense_schema.dump(expense)},HTTPStatus.OK

@expenses.delete("/expenses/<int:id>")
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
