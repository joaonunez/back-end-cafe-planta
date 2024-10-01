from flask import Blueprint, jsonify
from models.base import db
from models.cafe import Cafe

cafe = Blueprint("cafe", __name__, url_prefix="/cafe")

@cafe.route("/", methods=["GET"])
def get_cafes():
    cafes = Cafe.query.all()
    return jsonify([cafe.serialize() for cafe in cafes])
