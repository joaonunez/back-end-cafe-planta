from flask import Blueprint, jsonify
from models.base import db
from models.role import Role

role = Blueprint("role", __name__, url_prefix="/role")

@role.route("/", methods=["GET"])
def get_roles():
    roles = Role.query.all()
    return jsonify([role.serialize() for role in roles])
