from flask import Blueprint, request, jsonify
from extensions import db

from models.cafe import Cafe

cafe = Blueprint("cafe", __name__, url_prefix="/cafe")

@cafe.route("/", methods=["GET"])
def get_cafes():
    cafes = Cafe.query.all()
    return jsonify([cafe.serialize() for cafe in cafes])

@cafe.route('/', methods=['POST'])
def create_cafe():
    data = request.get_json()

    name = data.get('name')
    address = data.get('address')
    city_id = data.get('city_id')

    if not name or not address or not city_id:
        return jsonify({"error": "Name, address, and city_id are required"}), 400

    new_cafe = Cafe(name=name, address=address, city_id=city_id)
    db.session.add(new_cafe)
    db.session.commit()

    return jsonify(new_cafe.serialize()), 201