from flask import Blueprint, jsonify
from models import Venta
from models import db

venta = Blueprint("venta", __name__, url_prefix="/camping")

@venta.route("/venta", methods=["GET"])
def get_ventas():
    ventas = Venta.query.all()
    return jsonify([venta.serializar() for venta in ventas])
