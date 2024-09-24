from flask import Blueprint, jsonify
from models import TipoItem
from models import db

tipo_item = Blueprint("tipo_item", __name__, url_prefix="/camping")

@tipo_item.route("/tipo_item", methods=["GET"])
def get_tipo_items():
    items = TipoItem.query.all()
    return jsonify([item.serializar() for item in items])
