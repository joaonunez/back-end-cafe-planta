# Importación de dependencias
import os
from flask import Flask, request, jsonify
from extensions import db, migrate, cors, bcrypt, jwt
from models import *  # Importar todos los modelos desde models/__init__.py
from routes import benefit, benefit_user, cafe, product_rating, product_category, customer, combo_menu, combo_menu_detail, city, sale_detail, favorite, dining_area, country, product, state, role, item_type, user, sale
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, set_access_cookies
from werkzeug.exceptions import Unauthorized
from datetime import datetime, timedelta, timezone
app = Flask(__name__)

# Configuración de base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://root:kYkDChFJJaDcDvfMISLvVrnJzyDdFcPw@junction.proxy.rlwy.net:26699/railway"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super_secret"  # Cambiar en producción
app.config["SECRET_KEY"] = "super_super_secret"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]  # Usar cookies para tokens
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"  # Ruta de la cookie de acceso
app.config["JWT_COOKIE_SECURE"] = False  # Cambiar a True en producción para usar HTTPS
app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Deshabilitar CSRF para desarrollo, habilitar en producción
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Duración del token de acceso
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)  # Duración del token de refresco


##para conectarse en DBeaver: jdbc:postgresql://dpg-crqmshrv2p9s73ea70g0-a.oregon-postgres.render.com:5432/cafeplanta ((falta modificar))

# Inicialización de extensiones con la aplicación Flask
db.init_app(app)
migrate.init_app(app, db)
cors.init_app(app, resources={r"/*": {"origins": "http://localhost:3000"}},
              supports_credentials=True,
              allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
              expose_headers="Authorization")

bcrypt.init_app(app)
jwt.init_app(app)

# Middleware para renovar el token automáticamente si está a punto de expirar
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
@app.errorhandler(Unauthorized)
def handle_unauthorized(e):
    return jsonify({"error": "Invalid or expired token, please log in again."}), 401


# ------------------------------------
# ROUTES
# ------------------------------------
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

if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=3001, debug=True)
