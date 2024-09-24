from flask import Blueprint, request, jsonify
from models.base import db  # Importar db desde base.py
from models.producto import Producto  # Importar el modelo Producto

producto = Blueprint("producto", __name__, url_prefix="/camping")

@producto.route("/producto", methods=["GET"])
def get_productos():
    productos = Producto.query.all()
    return jsonify([producto.serializar() for producto in productos])
