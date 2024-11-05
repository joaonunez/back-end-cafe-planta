from flask import Blueprint, request, jsonify
from models import User
from extensions import db, bcrypt
from flask_jwt_extended import (
    create_access_token, set_access_cookies, get_jwt_identity, unset_jwt_cookies, jwt_required
)
from datetime import timedelta

user = Blueprint("user", __name__, url_prefix="/user")

@user.route("/admin-login", methods=["POST"])
def admin_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Buscar al usuario por nombre de usuario con role_id 1 para administrador
    user = User.query.filter_by(username=username, role_id=1).first()
    if not user:
        return jsonify({"error": "Administrador no encontrado o rol incorrecto"}), 404

    # Verificar la contraseña usando bcrypt
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Generar token de acceso con JWT
    access_token = create_access_token(identity=user.rut, expires_delta=timedelta(hours=1))

    # Serializar datos del usuario sin incluir la contraseña
    user_data = user.serialize()

    # Crear la respuesta con el token y los datos del usuario
    response = jsonify({
        "message": "Inicio de sesión exitoso",
        "user": user_data,
        "token": access_token
    })
    
    # Establecer el token en las cookies
    set_access_cookies(response, access_token)

    return response, 200

@user.route("/get_users_on_system", methods=["GET"])
def get_users_on_system():
    users = User.query.all()
    user_data = [user.serialize() for user in users]
    return jsonify(user_data), 200

@user.route("/logout-admin", methods=["POST"])
@jwt_required()  # Requiere que el usuario esté autenticado
def logout_admin():
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)  # Elimina las cookies JWT
    return response, 200