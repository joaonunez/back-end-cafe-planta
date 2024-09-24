from flask import Blueprint, request, jsonify
from models.base import db  # Importar db desde base.py
from models.venta import Venta  # Importar el modelo Venta

venta = Blueprint("venta", __name__, url_prefix="/camping")

@venta.route("/venta", methods=["GET"])
def get_ventas():
    ventas = Venta.query.all()
    return jsonify([venta.serializar() for venta in ventas])
