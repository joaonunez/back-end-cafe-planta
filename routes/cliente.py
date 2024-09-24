from flask import Blueprint, jsonify
from models import Cliente
from models import db

cliente = Blueprint("cliente", __name__, url_prefix="/clientes")

@cliente.route("/", methods=["GET"])
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([cliente.serializar() for cliente in clientes])
