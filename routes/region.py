from flask import Blueprint, request, jsonify
from models.base import db  # Importar db desde base.py
from models.region import Region  # Importar el modelo Region

region = Blueprint("region", __name__, url_prefix="/camping")

@region.route("/region", methods=["GET"])
def get_regiones():
    regiones = Region.query.all()
    return jsonify([region.serializar() for region in regiones])
