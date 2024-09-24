from flask import Blueprint, request, jsonify
from models.base import db  # Importar db desde base.py
from models.rol import Rol  # Importar el modelo Rol

rol = Blueprint("rol", __name__, url_prefix="/camping")

@rol.route("/rol", methods=["GET"])
def get_roles():
    roles = Rol.query.all()
    return jsonify([rol.serializar() for rol in roles])
