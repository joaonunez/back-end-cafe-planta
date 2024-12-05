from flask import Blueprint, request, jsonify
from extensions import db

from models.state import State

state = Blueprint('state', __name__, url_prefix='/state')

@state.route("/", methods=["GET"])
def get_states():
    states = State.query.all()
    return jsonify([state.serialize() for state in states])

@state.route('/bulk', methods=['POST'])
def create_states_bulk():
    data = request.get_json()
    
    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of regions"}), 400
    
    new_states = []
    
    for region in data:
        name = region.get('name')
        country_id = region.get('country_id')
        
        if not name or not country_id:
            return jsonify({"error": "Region name and country_id are required for all regions"}), 400
        
        new_state = State(name=name, country_id=country_id)
        db.session.add(new_state)
        new_states.append(new_state)
    
    db.session.commit()
    
    return jsonify([state.serialize() for state in new_states]), 201