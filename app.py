# Importación de dependencias
import os
import pymysql
import traceback
pymysql.install_as_MySQLdb()
from flask import Flask, request, jsonify
from extensions import db, migrate, cors, bcrypt, jwt
from models import *  # Importar todos los modelos desde models/__init__.py
from routes import benefit, benefit_user, cafe, product_rating, product_category, customer, combo_menu, combo_menu_detail, city, sale_detail, favorite, dining_area, country, product, state, role, item_type, user, sale
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, set_access_cookies
from werkzeug.exceptions import Unauthorized
from datetime import datetime, timedelta, timezone
from flask_talisman import Talisman  # Seguridad extra opcional

app = Flask(__name__)

# Configuración de base de datos (usando variable de entorno para mayor seguridad)
try:
    db_url = os.getenv("DATABASE_URL")
    print(f"Connecting to database at {db_url}")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
except Exception as e:
    print(f"Error in database connection: {str(e)}")
    traceback.print_exc()

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Claves secretas (usando variables de entorno para producción)
try:
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_jwt_secret_key")  # Default in case of missing
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")  # Default in case of missing
    print("Loaded JWT and Secret keys.")
except Exception as e:
    print(f"Error loading secret keys: {str(e)}")
    traceback.print_exc()

# Configuración de JWT para cookies
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
app.config["JWT_COOKIE_SECURE"] = True  # Asegurarse de que las cookies solo se envíen a través de HTTPS
app.config["JWT_COOKIE_CSRF_PROTECT"] = True  # Habilitar protección CSRF
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Duración del token de acceso
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)  # Duración del token de refresco

# Inicialización de extensiones con la aplicación Flask
try:
    db.init_app(app)
    migrate.init_app(app, db)
    print("Database and migration initialized successfully.")
except Exception as e:
    print(f"Error initializing database or migration: {str(e)}")
    traceback.print_exc()

# CORS: Configurar correctamente el dominio de tu frontend
try:
    frontend_origin = os.getenv("FRONTEND_ORIGIN", "https://cafe-planta-front-end-production.up.railway.app")
    cors.init_app(app, resources={r"/*": {"origins": frontend_origin}},
                  supports_credentials=True,
                  allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
                  expose_headers="Authorization")
    print(f"CORS configured with frontend origin: {frontend_origin}")
except Exception as e:
    print(f"Error configuring CORS: {str(e)}")
    traceback.print_exc()

bcrypt.init_app(app)
jwt.init_app(app)

# Seguridad extra con Talisman
try:
    Talisman(app)  # Aplica políticas de seguridad como HTTPS, HSTS, etc.
    print("Talisman configured for extra security.")
except Exception as e:
    print(f"Error configuring Talisman: {str(e)}")
    traceback.print_exc()

# Middleware para renovar el token automáticamente si está a punto de expirar
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        if datetime.timestamp(now + timedelta(minutes=15)) > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
    except (RuntimeError, KeyError) as e:
        print(f"Error in JWT token refresh: {str(e)}")
        # Ignorar si no hay token o no se puede actualizar
    return response

# Manejo de errores de autenticación
@app.errorhandler(Unauthorized)
def handle_unauthorized(e):
    return jsonify({"error": "Invalid or expired token, please log in again."}), 401

# Ruta para saludar
@app.route('/')
def hello():
    return '<h1>Hola, soy la API de Café Planta</h1>'

# ------------------------------------
# ROUTES
# ------------------------------------
try:
    app.register_blueprint(benefit)
    app.register_blueprint(benefit_user)
    app.register_blueprint(cafe)
    app.register_blueprint(product_rating)
    app.register_blueprint(product_category)
    app.register_blueprint(customer)
    app.register_blueprint(combo_menu)
    app.register_blueprint(combo_menu_detail)
    app.register_blueprint(city)
    app.register_blueprint(sale_detail)
    app.register_blueprint(favorite)
    app.register_blueprint(dining_area)
    app.register_blueprint(country)
    app.register_blueprint(product)
    app.register_blueprint(state)
    app.register_blueprint(role)
    app.register_blueprint(item_type)
    app.register_blueprint(user)
    app.register_blueprint(sale)
    print("All routes registered successfully.")
except Exception as e:
    print(f"Error registering routes: {str(e)}")
    traceback.print_exc()

if __name__ == '__main__':
    print("Starting the Flask app...")
    app.run(debug=True)
