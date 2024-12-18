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

@user.route("/delete/<string:rut>", methods=["DELETE"])
@jwt_required()
def delete_user(rut):
    # Obtenemos la identidad del JWT (rut del usuario logueado)
    current_user_rut = get_jwt_identity()
    current_user = User.query.filter_by(rut=current_user_rut).first()

    # Verificar que el usuario actual sea administrador
    if not current_user or current_user.role_id != 1:
        return jsonify({"error": "No está autorizado para eliminar usuarios"}), 403

    data = request.get_json()
    admin_rut = data.get("admin_rut")
    admin_password = data.get("password")

    # Verificar que el rut del admin coincida con el usuario logueado y que la contraseña sea correcta
    if current_user.rut != admin_rut:
        return jsonify({"error": "No coincide el rut del administrador"}), 401

    if not bcrypt.check_password_hash(current_user.password, admin_password):
        return jsonify({"error": "Contraseña de administrador incorrecta"}), 401

    # Buscar el usuario a eliminar
    user_to_delete = User.query.filter_by(rut=rut).first()
    if not user_to_delete:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Evitar que el administrador se elimine a sí mismo
    if user_to_delete.rut == current_user.rut:
        return jsonify({"error": "No puedes eliminar tu propia cuenta"}), 400

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify({"message": "Usuario eliminado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar el usuario: {str(e)}"}), 500

@user.route("/create-user", methods=["POST"])
@jwt_required()
def create_new_user():
    current_user_rut = get_jwt_identity()
    current_user = User.query.filter_by(rut=current_user_rut).first()

    # Validar que sea administrador
    if not current_user or current_user.role_id != 1:
        return jsonify({"error": "No está autorizado para crear usuarios"}), 403

    data = request.get_json()
    
    # Verificar que los campos requeridos estén presentes
    required_fields = ["rut", "first_name", "last_name_father", "last_name_mother", "username", "email", "password", "role_id", "cafe_id"]
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    # Verificar que el email o username no estén ya en uso
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": f"El email {data['email']} ya está en uso"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": f"El username {data['username']} ya está en uso"}), 400

    # Encriptar la contraseña
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')

    # Crear el usuario
    new_user = User(
        rut=data["rut"],
        first_name=data["first_name"],
        last_name_father=data["last_name_father"],
        last_name_mother=data["last_name_mother"],
        username=data["username"],
        email=data["email"],
        password=hashed_password,
        role_id=int(data["role_id"]),
        cafe_id=int(data["cafe_id"])
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuario creado exitosamente", "user": new_user.serialize()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear el usuario: {str(e)}"}), 500

@user.route("/change_password/<string:rut>", methods=["PUT"])
@jwt_required()
def change_user_password(rut):
    current_user_rut = get_jwt_identity()
    current_user = User.query.filter_by(rut=current_user_rut).first()

    # Verificar que es admin
    if not current_user or current_user.role_id != 1:
        return jsonify({"error": "No está autorizado para cambiar la contraseña"}), 403

    data = request.get_json()
    admin_rut = data.get("admin_rut")
    admin_password = data.get("admin_password")
    new_password = data.get("new_password")

    if not admin_rut or not admin_password or not new_password:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    if current_user.rut != admin_rut:
        return jsonify({"error": "RUT de administrador no coincide"}), 401

    if not bcrypt.check_password_hash(current_user.password, admin_password):
        return jsonify({"error": "Contraseña del administrador incorrecta"}), 401

    user_to_update = User.query.filter_by(rut=rut).first()
    if not user_to_update:
        return jsonify({"error": "Usuario no encontrado"}), 404

    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user_to_update.password = hashed_password

    try:
        db.session.commit()
        return jsonify({"message": "Contraseña cambiada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al cambiar la contraseña: {str(e)}"}), 500
