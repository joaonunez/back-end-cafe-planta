from flask import Blueprint, jsonify
from models.base import db
from models.item_type import ItemType

item_type = Blueprint("item_type", __name__, url_prefix="/item_type")

@item_type.route("/", methods=["GET"])
def get_item_types():
    types = ItemType.query.all()
    return jsonify([item_type.serialize() for item_type in types])
