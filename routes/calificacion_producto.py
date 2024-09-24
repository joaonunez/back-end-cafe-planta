from flask import Blueprint, request, jsonify
from models.base import db  # Importar db desde base.py
from models.calificacion_producto import CalificacionProducto  # Importar el modelo CalificacionProducto

calificacion_producto = Blueprint("calificacion_producto", __name__, url_prefix="/camping")

@calificacion_producto.route("/calificacion_producto", methods=["GET"])
def get_calificaciones():
    calificaciones = CalificacionProducto.query.all()
    return jsonify([calificacion.serializar() for calificacion in calificaciones])
