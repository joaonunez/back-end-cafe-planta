import os
from flask import Flask, request, jsonify
from extensions import db, migrate, cors, bcrypt, jwt
from models import *  # Importar todos los modelos desde models/__init__.py
from routes import (benefit, benefit_user, cafe, cart, product_rating, 
                    product_category, customer, combo_menu, 
                    combo_menu_detail, city, sale_detail, favorite, 
                    dining_area, country, product, state, role, 
                    item_type, user, sale, cloudinary_bp)
from flask_jwt_extended import (create_access_token, get_jwt, 
                                get_jwt_identity, set_access_cookies, unset_jwt_cookies)
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
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL no está configurado. Asegúrate de definirla en tu entorno de Vercel.")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ------------------------------------
    # CONFIGURACIÓN JWT
    # ------------------------------------
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super_secret")  # Cambiar en producción
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "super_super_secret")
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]  # Usar cookies para tokens
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"  # Ruta de la cookie de acceso
    app.config["JWT_COOKIE_SECURE"] = os.getenv("FLASK_ENV", "production") == "production"  # Cambiar a True en producción
    app.config["JWT_COOKIE_CSRF_PROTECT"] = True  # Habilitar en producción
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    # ------------------------------------
    # INICIALIZACIÓN DE EXTENSIONES
    # ------------------------------------
    try:
        db.init_app(app)
        migrate.init_app(app, db)
    except Exception as e:
        raise RuntimeError(f"Error inicializando la base de datos: {e}")

    cors.init_app(app, resources={r"/*": {"origins": "https://front-end-cafe-planta.vercel.app"}},
                  supports_credentials=True)

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
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, Access-Control-Allow-Credentials")
            response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
            response.headers.add("Access-Control-Allow-Origin", "https://front-end-cafe-planta.vercel.app")
            response.headers.add("Access-Control-Allow-Credentials", "true")
            return response

    # ------------------------------------
    # MANEJO DE ERRORES
    # ------------------------------------
    @app.errorhandler(Unauthorized)
    def handle_unauthorized(e):
        response = jsonify({"error": "Invalid or expired token, please log in again."})
        unset_jwt_cookies(response)  # Eliminar cookies en caso de token inválido
        return response, 401

    # ------------------------------------
    # CONFIGURACIÓN DE CLOUDINARY
    # ------------------------------------
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", "dsk6jeymj"),
        api_key=os.getenv("CLOUDINARY_API_KEY", "632813965993916"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET", "lSqeRpSRw4FNvCn3ew25hY3x-54")
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
    app.register_blueprint(cloudinary_bp)

    return app

# ------------------------------------
# EJECUCIÓN DE LA APLICACIÓN
# ------------------------------------
app = create_app()  # Cambiado para asegurar que Vercel lo detecte

if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 3001)))