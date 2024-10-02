from flask import Blueprint, request, jsonify
from models.base import db
from models.benefit_user import BenefitUser

benefit_user = Blueprint('benefit_user', __name__, url_prefix='/benefit_user')

@benefit_user.route('/bulk', methods=['POST'])
def assign_benefits_bulk():
    data = request.get_json()

    # Validar que se recibe una lista de asignaciones
    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of benefit assignments"}), 400

    new_assignments = []

    for assignment in data:
        benefit_id = assignment.get('benefit_id')
        user_rut = assignment.get('user_rut')

        # Validar que el benefit_id y user_rut estén presentes
        if not benefit_id or not user_rut:
            return jsonify({"error": "Missing benefit_id or user_rut in one or more assignments"}), 400

        # Verificar si la asignación ya existe
        existing_assignment = BenefitUser.query.filter_by(benefit_id=benefit_id, user_rut=user_rut).first()
        if existing_assignment:
            return jsonify({"error": f"Benefit {benefit_id} already assigned to user {user_rut}"}), 400

        # Crear la nueva asignación
        new_assignment = BenefitUser(benefit_id=benefit_id, user_rut=user_rut)
        db.session.add(new_assignment)
        new_assignments.append(new_assignment)

    # Confirmar los cambios en la base de datos
    db.session.commit()

    # Retornar la lista de asignaciones creadas
    return jsonify([assignment.serialize() for assignment in new_assignments]), 201
