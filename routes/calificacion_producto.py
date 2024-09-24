from flask import Blueprint, jsonify
from models import CalificacionProducto
from models import db

calificacion_producto = Blueprint("calificacion_producto", __name__, url_prefix="/calificacion-producto")

@calificacion_producto.route("/", methods=["GET"])
def get_calificaciones():
    calificaciones = CalificacionProducto.query.all()
    return jsonify([calificacion.serializar() for calificacion in calificaciones])
