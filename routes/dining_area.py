from flask import Blueprint, jsonify
from extensions import db
from models.dining_area import DiningArea

dining_area = Blueprint("dining_area", __name__, url_prefix="/dining_area")

@dining_area.route("/", methods=["GET"])
def get_dining_areas():
    areas = DiningArea.query.all()
    return jsonify([area.serialize() for area in areas])
