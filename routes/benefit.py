from flask import Blueprint, jsonify
from models.base import db
from models.benefit import Benefit

benefit = Blueprint("benefit", __name__, url_prefix="/benefit")

@benefit.route("/", methods=["GET"])
def get_benefits():
    benefits = Benefit.query.all()
    return jsonify([benefit.serialize() for benefit in benefits])
