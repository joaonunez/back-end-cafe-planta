from flask import Blueprint
from models import Beneficio
from flask import request, jsonify
from models import db

beneficio = Blueprint("beneficio", __name__, url_prefix="/camping")

@beneficio.route("/beneficio", methods=["GET"])
def get_beneficios():
    beneficios = Beneficio.query.all()
    return jsonify([beneficio.serialize() for beneficio in beneficios])