from flask import Blueprint, request, jsonify
from models.base import db  # Importar db desde base.py
from models.detalle_venta import DetalleVenta  # Importar el modelo DetalleVenta

detalle_venta = Blueprint("detalle_venta", __name__, url_prefix="/camping")

@detalle_venta.route("/detalle_venta", methods=["GET"])
def get_detalles_venta():
    detalles_venta = DetalleVenta.query.all()
    return jsonify([detalle.serializar() for detalle in detalles_venta])
