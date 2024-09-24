from flask import Blueprint, jsonify
from models import Producto
from models import db

producto = Blueprint("producto", __name__, url_prefix="/camping")

@producto.route("/producto", methods=["GET"])
def get_productos():
    productos = Producto.query.all()
    return jsonify([producto.serializar() for producto in productos])
