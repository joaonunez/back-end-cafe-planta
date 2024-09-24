from flask import Blueprint, request, jsonify
from models.base import db  # Importar db desde base.py
from models.beneficio import Beneficio  # Importar el modelo Beneficio

beneficio = Blueprint("beneficio", __name__, url_prefix="/camping")

@beneficio.route("/beneficio", methods=["GET"])
def get_beneficios():
    beneficios = Beneficio.query.all()
    return jsonify([beneficio.serializar() for beneficio in beneficios])
