from flask import Blueprint, jsonify
from models import Mesa
from models import db

mesa = Blueprint("mesa", __name__, url_prefix="/mesas")

@mesa.route("/", methods=["GET"])
def get_mesas():
    mesas = Mesa.query.all()
    return jsonify([mesa.serializar() for mesa in mesas])
