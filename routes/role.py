from flask import Blueprint, request, jsonify
from extensions import db

from models.role import Role


role = Blueprint("role", __name__, url_prefix="/role")

@role.route("/", methods=["GET"])
def get_roles():
    roles = Role.query.all()
    return jsonify([role.serialize() for role in roles])

@role.route('/bulk', methods=['POST'])
def create_roles_bulk():
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of roles"}), 400

    new_roles = []

    for role_data in data:
        name = role_data.get('name')
        base_salary = role_data.get('base_salary')

        if not name or base_salary is None:
            return jsonify({"error": "Name and base_salary are required for all roles"}), 400

        new_role = Role(name=name, base_salary=base_salary)
        db.session.add(new_role)
        new_roles.append(new_role)

    db.session.commit()

    return jsonify([role.serialize() for role in new_roles]), 201