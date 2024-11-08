from flask import Blueprint, request, jsonify
from models import User
from extensions import db, bcrypt
from flask_jwt_extended import (
    create_access_token, set_access_cookies, get_jwt_identity, unset_jwt_cookies, jwt_required
)
from datetime import timedelta

user = Blueprint("user", __name__, url_prefix="/user")

# Login de administrador
@user.route("/admin-login", methods=["POST"])
def admin_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username, role_id=1).first()
    if not user:
        return jsonify({"error": "Administrador no encontrado o rol incorrecto"}), 404
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Credenciales inválidas"}), 401
    access_token = create_access_token(identity=user.rut, expires_delta=timedelta(hours=1))
    user_data = user.serialize()
    response = jsonify({
        "message": "Inicio de sesión exitoso",
        "user": user_data,
        "token": access_token
    })
    set_access_cookies(response, access_token)
    return response, 200

# Login de empleado (vendedor)
@user.route("/employee-login", methods=["POST"])
def employee_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username, role_id=3).first()
    if not user:
        return jsonify({"error": "Vendedor no encontrado o rol incorrecto"}), 404
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Credenciales inválidas"}), 401
    access_token = create_access_token(identity=user.rut, expires_delta=timedelta(hours=1))
    user_data = user.serialize()
    response = jsonify({
        "message": "Inicio de sesión exitoso",
        "user": user_data,
        "token": access_token
    })
    set_access_cookies(response, access_token)
    return response, 200

# Logout de administrador
@user.route("/logout-admin", methods=["POST"])
@jwt_required()
def logout_admin():
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200

# Logout de empleado (vendedor)
@user.route("/logout-employee", methods=["POST"])
@jwt_required()
def logout_employee():
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200
