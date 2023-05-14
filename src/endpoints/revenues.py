from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
from src.database import db
import werkzeug
from datetime import datetime, timedelta
from src.models.revenue import Revenue, revenue_schema, revenues_schema
from src.endpoints.users import read_user
from flask_jwt_extended import jwt_required,get_jwt_identity


revenues = Blueprint("revenues",__name__,url_prefix="/api/v1/revenues")

@revenues.get("/consulta")
def consulta_fecha():
    user = read_user()[0]['data']
    print(f'datos usuario: {user}')
    userDocument = user['document']

    inicio = datetime.strptime(request.args.get('inicio'), '%Y-%m-%d')
    fin = datetime.strptime(request.args.get('fin'), '%Y-%m-%d')

    print(f'Los datos de consulta son: {userDocument}, {inicio}, {fin}')

    revenue = Revenue.query.order_by(Revenue.id).filter(Revenue.user_document==userDocument,Revenue.date_hour >= inicio, Revenue.date_hour < fin + timedelta(days=1)).all()

    return {"data": revenues_schema.dump(revenue)}, HTTPStatus.OK

''' Listar todos los ingresos perdenecientes al usuario que se encuentra autenticado '''
@revenues.get("/")
def read_revenues():
    user = read_user()[0]['data']
    print(f'datos usuario: {user}')
    userDocument = user['document']

    revenue = Revenue.query.filter_by(user_document=userDocument).all()
    if(not revenue):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND

    return {"data":revenues_schema.dump(revenue)},HTTPStatus.OK
''' Listar un ingreso perdeneciente al usuario que se encuentra autenticado '''
@revenues.get("/<int:id>")
def read_revenue(id):
    revenue = Revenue.query.filter_by(id=id).one_or_none()
    if(not revenue):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    return {"data":revenue_schema.dump(revenue)},HTTPStatus.OK

@revenues.get("/c")
def read_all():
    revenue = Revenue.query.order_by(Revenue.id).all()
    return {"data": revenues_schema.dump(revenue)}, HTTPStatus.OK
''' Crear un ingreso perdeneciente al usuario que se encuentra autenticado '''
@revenues.post("/")
def create():
    post_data = None
    user = read_user()[0]['data']
    userDocument = user['document']
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Post body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST

    date_hour = Revenue.parse_date_hour(request.get_json().get("date_hour",None))

    revenue = Revenue(
                date_hour = date_hour,
                value = request.get_json().get("value",None),
                cumulative = request.get_json().get("cumulative",None),
                user_document = userDocument)

    try:
        db.session.add(revenue)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":revenue_schema.dump(revenue)},HTTPStatus.CREATED

''' Actualizar un ingreso perdeneciente al usuario que se encuentra autenticado'''
@revenues.put("/<int:id>")
def update_revenue(id):
    post_data = None

    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error":"Put body JSON data not found","message":str(e)},HTTPStatus.BAD_REQUEST

    revenue = Revenue.query.filter_by(id=id).one_or_none()

    if (not revenue):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND


    revenue.date_hour = Revenue.parse_date_hour(request.get_json().get("date_hour",revenue.date_hour))
    revenue.value = request.get_json().get("value",revenue.value)
    revenue.cumulative = request.get_json().get("cumulative",revenue.cumulative)

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST

    return {"data":revenue_schema.dump(revenue)},HTTPStatus.OK
''' Eliminar un ingreso'''
@revenues.delete("/<int:id>")
def delete(id):
    revenue = Revenue.query.filter_by(id=id).one_or_none()
    if (not revenue):
        return {"error":"Resource not found"}, HTTPStatus.NOT_FOUND
    try:
        db.session.delete(revenue)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error":"Invalid resource values","message":str(e)},HTTPStatus.BAD_REQUEST
    return {"data":revenue_schema.dump(revenue)},HTTPStatus.NO_CONTENT
