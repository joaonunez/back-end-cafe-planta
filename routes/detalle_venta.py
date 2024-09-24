from flask import Blueprint, jsonify
from models import DetalleVenta
from models import db

detalle_venta = Blueprint("detalle_venta", __name__, url_prefix="/camping")

@detalle_venta.route("/detalle_venta", methods=["GET"])
def get_detalle_ventas():
    detalles = DetalleVenta.query.all()
    return jsonify([detalle.serializar() for detalle in detalles])
