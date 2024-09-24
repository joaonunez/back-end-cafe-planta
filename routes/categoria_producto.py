from flask import Blueprint, request, jsonify
from models.base import db  # Importar db desde base.py
from models.categoria_producto import CategoriaProducto  # Importar el modelo CategoriaProducto

categoria_producto = Blueprint("categoria_producto", __name__, url_prefix="/camping")

@categoria_producto.route("/categoria_producto", methods=["GET"])
def get_categorias():
    categorias = CategoriaProducto.query.all()
    return jsonify([categoria.serializar() for categoria in categorias])
