from flask import Blueprint, jsonify
from models import Comuna
from models import db

comuna = Blueprint("comuna", __name__, url_prefix="/camping")

@comuna.route("/comuna", methods=["GET"])
def get_comunas():
    comunas = Comuna.query.all()
    return jsonify([comuna.serializar() for comuna in comunas])
