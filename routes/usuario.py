from flask import Blueprint, request, jsonify
from models.base import db  # Importar db desde base.py
from models.usuario import Usuario  # Importar el modelo Usuario

usuario = Blueprint("usuario", __name__, url_prefix="/camping")

@usuario.route("/usuario", methods=["GET"])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([usuario.serializar() for usuario in usuarios])
