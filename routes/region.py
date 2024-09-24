from flask import Blueprint, jsonify
from models import Region
from models import db

region = Blueprint("region", __name__, url_prefix="/camping")

@region.route("/region", methods=["GET"])
def get_regiones():
    regiones = Region.query.all()
    return jsonify([region.serializar() for region in regiones])
