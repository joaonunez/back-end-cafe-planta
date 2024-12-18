from flask import Blueprint, request, jsonify
from extensions import db

from models.role import Role


role = Blueprint("role", __name__, url_prefix="/role")

@role.route("/", methods=["GET"])
def get_roles():
    roles = Role.query.all()
    roles_data = [{"id": r.id, "name": r.name} for r in roles]
    return jsonify(roles_data), 200