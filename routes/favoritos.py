from flask import Blueprint, request, jsonify
from models.base import db  # Importar db desde base.py
from models.favoritos import Favoritos  # Importar el modelo Favoritos

favoritos = Blueprint("favoritos", __name__, url_prefix="/camping")

@favoritos.route("/favoritos", methods=["GET"])
def get_favoritos():
    favoritos_lista = Favoritos.query.all()
    return jsonify([favorito.serializar() for favorito in favoritos_lista])
