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

# Ruta para obtener todos los usuarios en el sistema
@user.route("/get_users_on_system", methods=["GET"])
@jwt_required()
def get_users_on_system():
    try:
        # Obtiene todos los usuarios de la base de datos
        users = User.query.all()
        
        # Serializa cada usuario para devolver los datos en formato JSON
        users_data = [user.serialize() for user in users]
        return jsonify(users_data), 200
    except Exception as e:
        print("Error al obtener usuarios en el sistema:", e)
        return jsonify({"error": "Error al obtener usuarios"}), 500


@user.route("/edit/<string:rut>", methods=["PUT"])
@jwt_required()
def edit_user(rut):
    # Obtenemos la identidad del JWT
    current_user_rut = get_jwt_identity()
    current_user = User.query.filter_by(rut=current_user_rut).first()

    if not current_user or current_user.role_id != 1:
        return jsonify({"error": "No está autorizado para editar usuarios"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibieron datos para actualizar"}), 400

    user_to_edit = User.query.filter_by(rut=rut).first()
    if not user_to_edit:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Lista de campos permitidos para actualizar
    allowed_fields = ["first_name", "last_name_father", "last_name_mother", "username", "email", "role_id", "cafe_id"]
    for field in allowed_fields:
        if field in data and data[field] is not None:
            setattr(user_to_edit, field, data[field])

    try:
        db.session.commit()
        return jsonify({"message": "Usuario actualizado exitosamente", "user": user_to_edit.serialize()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al actualizar el usuario: {str(e)}"}), 500
