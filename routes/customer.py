#customer.py
from flask import Blueprint, request, jsonify
from models import Customer
from extensions import bcrypt, db
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, unset_jwt_cookies
customer = Blueprint("customer", __name__, url_prefix="/customer")

@customer.route("/", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.serialize() for customer in customers])

@customer.route("/bulk", methods=["POST"])
def create_customers_bulk():
    data = request.get_json()

    # Validar que se recibe una lista de clientes
    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of customers"}), 400

    new_customers = []

    for customer_data in data:
        # Validar que los campos requeridos están presentes
        if not all([
            customer_data.get("rut"),
            customer_data.get("name"),
            customer_data.get("email"),
            customer_data.get("username"),
            customer_data.get("password")
        ]):
            return jsonify({"error": "Missing required fields for one or more customers"}), 400

        # Verificar si el email o username ya están en uso
        if Customer.query.filter_by(email=customer_data["email"]).first():
            return jsonify({"error": f"Email {customer_data['email']} already in use"}), 400

        if Customer.query.filter_by(username=customer_data["username"]).first():
            return jsonify({"error": f"Username {customer_data['username']} already in use"}), 400

        # Encriptar la contraseña usando bcrypt
        hashed_password = bcrypt.generate_password_hash(customer_data["password"]).decode('utf-8')

        # Crear el nuevo cliente
        new_customer = Customer(
            rut=customer_data["rut"],
            name=customer_data["name"],
            email=customer_data["email"],
            username=customer_data["username"],
            password=hashed_password  # Guardar la contraseña encriptada
        )
        db.session.add(new_customer)
        new_customers.append(new_customer)

    # Confirmar los cambios en la base de datos
    db.session.commit()

    # Retornar la lista de clientes creados
    return jsonify([customer.serialize() for customer in new_customers]), 201

@customer.route("/login-customer", methods=["POST"])
def login_customer():
    # Obtener los datos enviados en la solicitud
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    # Buscar al cliente por nombre de usuario
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({"error": "Cliente no encontrado"}), 404
    
    # Verificar la contraseña usando bcrypt de extensions
    if not bcrypt.check_password_hash(customer.password, password):
        return jsonify({"error": "Credenciales Invalidas"}), 401
    
    # Generar token de acceso con JWT usando el RUT del cliente
    access_token = create_access_token(identity=customer.rut)
    
    # Serializar datos del customer (sin incluir la contraseña)
    customer_data = customer.serialize()

    # Crear la respuesta con el token y los datos del cliente
    response = jsonify({
        "message": "Login successful",
        "customer": customer_data,
        "token": access_token
    })
    
    # Establecer el token en las cookies
    set_access_cookies(response, access_token)
    
    # Devolver la respuesta con estado 200
    return response, 200

@customer.route("/register-customer", methods=["POST"])
def register_customer():
    data = request.get_json()
    
    # Validar campos requeridos
    if not all([data.get("rut"), data.get("name"), data.get("email"), data.get("username"), data.get("password")]):
        return jsonify({"error": "Missing required fields"}), 400

    # Verificar si el email o username ya están en uso
    if Customer.query.filter_by(email=data["email"]).first():
        return jsonify({"error": f"Email {data['email']} already in use"}), 400

    if Customer.query.filter_by(username=data["username"]).first():
        return jsonify({"error": f"Username {data['username']} already in use"}), 400

    # Encriptar la contraseña usando bcrypt
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')

    # Crear nuevo cliente
    new_customer = Customer(
        rut=data["rut"],
        name=data["name"],
        email=data["email"],
        username=data["username"],
        password=hashed_password  # Guardar la contraseña encriptada
    )

    db.session.add(new_customer)
    db.session.commit()

    return jsonify(new_customer.serialize()), 201

@customer.route("/logout-customer", methods=["POST"])
@jwt_required()  # Requiere autenticación para acceder al logout
def logout_customer():
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)  # Elimina las cookies JWT
    return response, 200