from flask import Blueprint, jsonify
from models import Cafeteria
from models import db

cafeteria = Blueprint("cafeteria", __name__, url_prefix="/camping")

@cafeteria.route("/cafeteria", methods=["GET"])
def get_cafeterias():
    cafeterias = Cafeteria.query.all()
    return jsonify([cafeteria.serializar() for cafeteria in cafeterias])
