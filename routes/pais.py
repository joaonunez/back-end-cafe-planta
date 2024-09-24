from flask import Blueprint, jsonify
from models import Pais
from models import db

pais = Blueprint("pais", __name__, url_prefix="/camping")

@pais.route("/pais", methods=["GET"])
def get_paises():
    paises = Pais.query.all()
    return jsonify([pais.serializar() for pais in paises])
