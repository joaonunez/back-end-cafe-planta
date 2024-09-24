from flask import Blueprint, request, jsonify
from models.base import db  # Importar db desde base.py
from models.cafeteria import Cafeteria  # Importar el modelo Cafeteria

cafeteria = Blueprint("cafeteria", __name__, url_prefix="/camping")

@cafeteria.route("/cafeteria", methods=["GET"])
def get_cafeterias():
    cafeterias = Cafeteria.query.all()
    return jsonify([cafeteria.serializar() for cafeteria in cafeterias])
