from flask import Blueprint, jsonify
from models.base import db
from models.state import State

state = Blueprint("state", __name__, url_prefix="/state")

@state.route("/", methods=["GET"])
def get_states():
    states = State.query.all()
    return jsonify([state.serialize() for state in states])
