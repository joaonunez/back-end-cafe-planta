from flask import Blueprint, jsonify
from models import Usuario
from models import db

usuario = Blueprint("usuario", __name__, url_prefix="/camping")

@usuario.route("/usuario", methods=["GET"])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([usuario.serializar() for usuario in usuarios])
