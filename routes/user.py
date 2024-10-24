#user.py
from flask import Blueprint, request, jsonify
from models import User
from extensions import db

from datetime import datetime
from extensions import bcrypt
from flask_jwt_extended import create_access_token, set_access_cookies

user = Blueprint("user", __name__, url_prefix="/user")

@user.route("/", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])

@user.route("/bulk", methods=["POST"])
def create_users_bulk():
    data = request.get_json()

    # Validar que se recibe una lista de usuarios
    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of users"}), 400

    new_users = []

    for user_data in data:
        # Validar que los campos requeridos están presentes
        if not all([
            user_data.get("rut"),
            user_data.get("first_name"),
            user_data.get("last_name_father"),
            user_data.get("last_name_mother"),
            user_data.get("username"),
            user_data.get("email"),
            user_data.get("password"),
            user_data.get("role_id"),
            user_data.get("cafe_id")
        ]):
            return jsonify({"error": "Missing required fields for one or more users"}), 400

        # Verificar si el email o username ya están en uso
        if User.query.filter_by(email=user_data["email"]).first():
            return jsonify({"error": f"Email {user_data['email']} already in use"}), 400

        if User.query.filter_by(username=user_data["username"]).first():
            return jsonify({"error": f"Username {user_data['username']} already in use"}), 400

        # Encriptar la contraseña usando bcrypt
        hashed_password = bcrypt.generate_password_hash(user_data["password"]).decode('utf-8')

        # Crear el nuevo usuario
        new_user = User(
            rut=user_data["rut"],
            first_name=user_data["first_name"],
            last_name_father=user_data["last_name_father"],
            last_name_mother=user_data["last_name_mother"],
            username=user_data["username"],
            email=user_data["email"],
            password=hashed_password,  # Guardar la contraseña encriptada
            role_id=user_data["role_id"],
            cafe_id=user_data["cafe_id"]
        )
        db.session.add(new_user)
        new_users.append(new_user)

    # Confirmar los cambios en la base de datos
    db.session.commit()

    # Retornar la lista de usuarios creados
    return jsonify([user.serialize() for user in new_users]), 201


@user.route("/login-user", methods=["POST"])
def login_customer():
    # Obtener los datos enviados en la solicitud
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    # Buscar al usuario por nombre de usuario
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Usuario Del Sitema no encontrado"}), 404
    
    # Verificar la contraseña usando bcrypt de extensions
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Credenciales Invalidas"}), 401
    
    # Generar token de acceso con JWT usando el RUT del usuario
    access_token = create_access_token(identity=user.rut)
    
    # Serializar datos del usuario (sin incluir la contraseña)
    user_data = user.serialize()

    # Crear la respuesta con el token y los datos del usuario
    response = jsonify({
        "message": "Login successful",
        "user": user_data,
        "token": access_token
    })
    
    # Establecer el token en las cookies
    set_access_cookies(response, access_token)
    
    # Devolver la respuesta con estado 200
    return response, 200