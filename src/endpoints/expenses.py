from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
from src.database import db
import werkzeug

from src.models.expense import Expense, expenses_schema, expensess_schema

expenses = Blueprint("expensess",__name__,url_prefix="/api/v1")

@expenses.get("/expenses")
def read_all():
 expense = Expense.query.order_by(Expense.id).all()
 return {"data": expenses_schema.dump(expense)}, HTTPStatus.OK

@expenses.get("/expenses/<int:id>")
def read_one(id):
    expense = Expense.query.filter_by(id=id).first()

    if(not expense):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    return {"data":expenses_schema.dump(expense)},HTTPStatus.OK


@expenses.post("/users/<int:user_id>/expenses")
def create(user_id):
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Post body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST

    expense = Expense(date_hour = request.get_json().get("date_hour",None),
                value = request.get_json().get("value",None),
                cumulative = request.get_json().get("cumulative",None),
                user_id = user_id)

    try:
        db.session.add(expense)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":expenses_schema.dump(expense)},HTTPStatus.CREATED

#@expenses.patch('/<int:id>')
@expenses.put('/users/<int:user_id>/expenses/<int:id>')
def update(id,user_id):
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Put body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST

    expense = Expense.query.filter_by(id=id).first()

    if (not expense):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    expense.date_hour = request.get_json().get("address",expense.date_hpur)
    expense.value = request.get_json().get("value",expense.value)
    expense.cumulative = request.get_json().get("flour_count",expense.flour_count)

    if (user_id != expense.user_id):
        expense.user_id = user_id

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":expenses_schema.dump(expense)},HTTPStatus.OK

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

    return {"data":expenses_schema.dump(expense)},HTTPStatus.NO_CONTENT
