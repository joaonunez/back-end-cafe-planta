from flask import Blueprint, jsonify
from models import Rol
from models import db

rol = Blueprint("rol", __name__, url_prefix="/camping")

@rol.route("/rol", methods=["GET"])
def get_roles():
    roles = Rol.query.all()
    return jsonify([rol.serializar() for rol in roles])
