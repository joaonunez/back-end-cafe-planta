from flask import Blueprint, request, jsonify
from models.base import db  # Importar db desde base.py
from models.mesa import Mesa  # Importar el modelo Mesa

mesa = Blueprint("mesa", __name__, url_prefix="/camping")

@mesa.route("/mesa", methods=["GET"])
def get_mesas():
    mesas = Mesa.query.all()
    return jsonify([mesa.serializar() for mesa in mesas])
