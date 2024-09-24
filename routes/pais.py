from flask import Blueprint, request, jsonify
from models.base import db  # Importar db desde base.py
from models.pais import Pais  # Importar el modelo Pais

pais = Blueprint("pais", __name__, url_prefix="/camping")

@pais.route("/pais", methods=["GET"])
def get_paises():
    paises = Pais.query.all()
    return jsonify([pais.serializar() for pais in paises])
