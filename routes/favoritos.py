from flask import Blueprint, jsonify
from models import Favoritos
from models import db

favoritos = Blueprint("favoritos", __name__, url_prefix="/favoritos")

@favoritos.route("/", methods=["GET"])
def get_favoritos():
    favoritos = Favoritos.query.all()
    return jsonify([favorito.serializar() for favorito in favoritos])
