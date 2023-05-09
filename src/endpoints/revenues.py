from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
from src.database import db
import werkzeug
from datetime import datetime
from src.models.revenue import Revenue, revenue_schema, revenues_schema

revenues = Blueprint("revenue",__name__,url_prefix="/api/v1")

@revenues.get("/revenues")
def read_all():
    revenue = Revenue.query.order_by(Revenue.id).all()
    return {"data": revenues_schema.dump(revenue)}, HTTPStatus.OK

@revenues.get("/revenues/<int:id>")
def read_one(id):
    revenue = Revenue.query.filter_by(id=id).first()

    if(not revenue):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    return {"data":revenue_schema.dump(revenue)},HTTPStatus.OK


@revenues.post("/users/<int:user_document>/revenues")
def create(user_document):
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Post body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST

    date_hour = request.get_json().get("date_hour",None)
    date_hour_ = datetime.strptime(date_hour, '%Y-%m-%d %H:%M').date()

    revenue = Revenue(
                date_hour = date_hour_,
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
@revenues.put('/users/<int:user_document>/revenues/<int:id>')
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

@revenues.delete("/revenues/<int:id>")
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
