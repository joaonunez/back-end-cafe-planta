from flask import Blueprint, jsonify
from models import CategoriaProducto
from models import db

categoria_producto = Blueprint("categoria_producto", __name__, url_prefix="/camping")

@categoria_producto.route("/categoria_producto", methods=["GET"])
def get_categoria_productos():
    categorias = CategoriaProducto.query.all()
    return jsonify([categoria.serializar() for categoria in categorias])
