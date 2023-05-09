from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
from src.database import db
import werkzeug
from flask_jwt_extended import jwt_required

from src.models.product import Product,product_schema,products_schema

products = Blueprint("products",__name__,url_prefix="/api/v1/products")

@products.get("/")
def read_all():
    products = Product.query.order_by(Product.name).all()
    return {"data": products_schema.dump(products)}, HTTPStatus.OK

@products.get("/<int:id>")
@jwt_required()
def read_one(id):
    for product in product_data:
        if product['id'] == id:
            return {"data": product}, HTTPStatus.OK

    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

@products.post("/")
def create():
    post_data = request.get_json()

    product = {
    "id": len(product_data) + 1,
    "name": post_data.get('name', 'No Name'),
    "price": post_data.get('price', 0),
    "expiration": post_data.get('expiration', None)
    }

    product_data.append(product)

    return {"data": product}, HTTPStatus.CREATED


@products.put('/<int:id>')
@products.patch('/<int:id>')
def update(id):
    post_data = request.get_json()
    for i in range(len(product_data)):
        if product_data[i]['id'] == id:
            product_data[i] = {
            "id": id,
            "name": post_data.get('name'),
            "price": post_data.get('price'),
            "expiration": post_data.get('expiration')
        }
        return {"data": product_data[i]}, HTTPStatus.OK
    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

@products.delete("/<int:id>")
def delete(id):
    for i in range(len(product_data)):
        if product_data[i]['id'] == id:
            del product_data[i]
            return {"data": ""}, HTTPStatus.NO_CONTENT
    return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND

#Proveedores de un producto
@products.get("/<int:id_producto>/providers")
def read_providers(id):
    pass
