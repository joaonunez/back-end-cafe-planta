from flask import Blueprint, request, jsonify
from models.base import db  # Importar db desde base.py
from models.rol import Rol  # Importar el modelo Rol

rol = Blueprint("rol", __name__, url_prefix="/rol")


@rol.route("/view-roles", methods=["GET"])
def get_roles():
    roles = Rol.query.all()
    return jsonify([rol.serializar() for rol in roles])

@rol.route("/add-role", methods=["POST"])
def create_rol():
    data = request.get_json()  # Obtener los datos JSON del cuerpo de la solicitud
    print("Datos recibidos:", data)  # Agregar esto para ver qué datos llegan
    if not data:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    nombre = data.get("nombre")
    salario_base = data.get("salario_base")

    # Validar los datos
    if not nombre or not salario_base:
        return jsonify({"error": "Los campos 'nombre' y 'salario_base' son requeridos"}), 400

    # Crear un nuevo objeto Rol
    nuevo_rol = Rol(nombre=nombre, salario_base=salario_base)

    # Agregar y confirmar la transacción
    try:
        db.session.add(nuevo_rol)
        db.session.commit()
        return jsonify({"message": "Rol creado exitosamente", "rol": nuevo_rol.serializar()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "No se pudo crear el rol", "details": str(e)}), 500