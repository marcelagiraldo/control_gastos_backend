from flask import Blueprint
providers = Blueprint("providers",__name__,url_prefix="/api/v1/providers")

#Ver productos de un proveedor
@providers.get("/<int:id>/products")
def read_products_from_providers(id):
 return "Reading products from providers ... soon"
