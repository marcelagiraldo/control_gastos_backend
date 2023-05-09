from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
from src.database import db
import werkzeug

from src.models.revenue import Revenue, revenue_schema, revenues_schema

revenue = Blueprint("revenue",__name__,url_prefix="/api/v1")

@revenue.get("/revenue")
def read_all():
 revenue = Revenue.query.order_by(Revenue.address).all()
 return {"data": revenue_schema.dump(revenue)}, HTTPStatus.OK

@revenue.get("/revenue/<int:id>")
def read_one(id):
    revenue = Revenue.query.filter_by(id=id).first()

    if(not revenue):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    return {"data":revenue_schema.dump(revenue)},HTTPStatus.OK


@revenue.post("/users/<int:user_document>/revenue")
def create(user_document):
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Post body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST

    revenue = Revenue(date_hour = request.get_json().get("date_hour",None),
                value = request.get_json().get("value",None),
                cumulative = request.get_json().get("cumulative",None),
                user_document = user_document)

    try:
        db.session.add(revenue)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":revenue_schema.dump(revenue)},HTTPStatus.CREATED

#@revenue.patch('/<int:id>')
@revenue.put('/users/<int:user_document>/revenue/<int:id>')
def update(id,user_document):
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Put body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST

    revenue = Revenue.query.filter_by(id=id).first()

    if (not revenue):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    revenue.date_hour = request.get_json().get("date_hour",revenue.date_hour)
    revenue.value = request.get_json().get("value",revenue.value)
    revenue.cumulative = request.get_json().get("cumulative",revenue.cumulative)

    if (user_document != revenue.user_document):
        revenue.user_document = user_document

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":revenue_schema.dump(revenue)},HTTPStatus.OK

@revenue.delete("/revenue/<int:id>")
def delete(id):
    revenue = Revenue.query.filter_by(id=id).first()
    if (not revenue):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    try:
        db.session.delete(revenue)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":revenue_schema.dump(revenue)},HTTPStatus.NO_CONTENT
