import os
from flask import Flask, request, jsonify
from extensions import db, migrate, cors, bcrypt, jwt
from models import *  # Importar todos los modelos desde models/__init__.py
from routes import (benefit, benefit_user, cafe, cart, product_rating, 
                    product_category, customer, combo_menu, 
                    combo_menu_detail, city, sale_detail, favorite, 
                    dining_area, country, product, state, role, 
                    item_type, user, sale)
from flask_jwt_extended import (create_access_token, get_jwt, 
                                get_jwt_identity, set_access_cookies)
from werkzeug.exceptions import Unauthorized
from datetime import datetime, timedelta, timezone
import cloudinary
import cloudinary.uploader

# ------------------------------------
# FACTORY DE CREACIÓN DE FLASK APP
# ------------------------------------
def create_app(config_name="default"):
    app = Flask(__name__)

    # ------------------------------------
    # CONFIGURACIÓN DE BASE DE DATOS
    # ------------------------------------
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", 
        "mysql+pymysql://root:kYkDChFJJaDcDvfMISLvVrnJzyDdFcPw@junction.proxy.rlwy.net:26699/railway"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ------------------------------------
    # CONFIGURACIÓN JWT
    # ------------------------------------
    app.config["JWT_SECRET_KEY"] = "super_secret"  # Cambiar en producción
    app.config["SECRET_KEY"] = "super_super_secret"
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]  # Usar cookies para tokens
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"  # Ruta de la cookie de acceso
    app.config["JWT_COOKIE_SECURE"] = False  # Cambiar a True en producción para usar HTTPS
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Habilitar en producción
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    # ------------------------------------
    # INICIALIZACIÓN DE EXTENSIONES
    # ------------------------------------
    db.init_app(app)
    migrate.init_app(app, db)

    # Configurar CORS con soporte para credenciales
    cors.init_app(app, resources={r"/*": {"origins": "http://localhost:3000"}},
                  supports_credentials=True,
                  allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
                  expose_headers="Authorization")

    bcrypt.init_app(app)
    jwt.init_app(app)

    # ------------------------------------
    # MIDDLEWARE JWT RENOVACIÓN DE TOKENS
    # ------------------------------------
    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            if datetime.timestamp(now + timedelta(minutes=15)) > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
        except (RuntimeError, KeyError):
            pass  # Ignorar si no hay token o no se puede actualizar
        return response

    # ------------------------------------
    # MANEJO DE SOLICITUDES OPTIONS PARA CORS
    # ------------------------------------
    @app.before_request
    def handle_options_requests():
        if request.method == 'OPTIONS':
            response = app.make_response('')
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
            response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
            response.headers.add("Access-Control-Allow-Credentials", "true")
            return response

    # ------------------------------------
    # MANEJO DE ERRORES
    # ------------------------------------
    @app.errorhandler(Unauthorized)
    def handle_unauthorized(e):
        return jsonify({"error": "Invalid or expired token, please log in again."}), 401

    # ------------------------------------
    # CONFIGURACIÓN DE CLOUDINARY
    # ------------------------------------
    cloudinary.config(
        cloud_name="dsk6jeymj",
        api_key="632813965993916",
        api_secret="lSqeRpSRw4FNvCn3ew25hY3x-54"
    )

    # ------------------------------------
    # REGISTRO DE RUTAS
    # ------------------------------------
    app.register_blueprint(benefit)
    app.register_blueprint(benefit_user)
    app.register_blueprint(cafe)
    app.register_blueprint(cart)
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

    return app

# ------------------------------------
# EJECUCIÓN DE LA APLICACIÓN
# ------------------------------------
if __name__ == "__main__": 
    app = create_app()
    app.run(host="0.0.0.0", port=3001, debug=True)
