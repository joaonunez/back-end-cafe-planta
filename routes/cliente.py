from flask import Blueprint, request, jsonify
from models.base import db  # Importar db desde base.py
from models.cliente import Cliente  # Importar el modelo Cliente

cliente = Blueprint("cliente", __name__, url_prefix="/camping")

@cliente.route("/cliente", methods=["GET"])
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([cliente.serializar() for cliente in clientes])
