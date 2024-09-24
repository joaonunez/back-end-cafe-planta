from flask import Blueprint, request, jsonify
from models.base import db  # Importar db desde base.py
from models.tipo_item import TipoItem  # Importar el modelo TipoItem

tipo_item = Blueprint("tipo_item", __name__, url_prefix="/camping")

@tipo_item.route("/tipo_item", methods=["GET"])
def get_tipos_item():
    tipos = TipoItem.query.all()
    return jsonify([tipo.serializar() for tipo in tipos])
