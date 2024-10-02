from flask import Blueprint, request, jsonify
from models.base import db
from models.item_type import ItemType

item_type = Blueprint("item_type", __name__, url_prefix="/item_type")

@item_type.route("/", methods=["GET"])
def get_item_types():
    types = ItemType.query.all()
    return jsonify([item_type.serialize() for item_type in types])

@item_type.route('/bulk', methods=['POST'])
def create_item_types_bulk():
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of item types"}), 400

    new_item_types = []

    for item_type_data in data:
        name = item_type_data.get('name')

        if not name:
            return jsonify({"error": "Missing 'name' field"}), 400

        new_item_type = ItemType(name=name)
        db.session.add(new_item_type)
        new_item_types.append(new_item_type)

    db.session.commit()

    return jsonify([item_type.serialize() for item_type in new_item_types]), 201