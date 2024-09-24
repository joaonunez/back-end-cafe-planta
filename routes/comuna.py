from flask import Blueprint, request, jsonify
from models.base import db  # Importar db desde base.py
from models.comuna import Comuna  # Importar el modelo Comuna

comuna = Blueprint("comuna", __name__, url_prefix="/camping")

@comuna.route("/comuna", methods=["GET"])
def get_comunas():
    comunas = Comuna.query.all()
    return jsonify([comuna.serializar() for comuna in comunas])
