# Importación de dependencias
import os
import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, request, jsonify
from extensions import db, migrate, cors, bcrypt, jwt
from models import *  # Importar todos los modelos desde models/__init__.py
from routes import benefit, benefit_user, cafe, product_rating, product_category, customer, combo_menu, combo_menu_detail, city, sale_detail, favorite, dining_area, country, product, state, role, item_type, user, sale
from werkzeug.exceptions import Unauthorized
from datetime import timedelta

app = Flask(__name__)

# Configuración de base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://root:kYkDChFJJaDcDvfMISLvVrnJzyDdFcPw@junction.proxy.rlwy.net:26699/railway"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Claves secretas
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "supersecretkey")  # Cambiar esto en producción
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "anothersecretkey")

# Configuración de JWT
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

# Inicialización de extensiones
db.init_app(app)
migrate.init_app(app, db)

# CORS: Permitir el acceso desde tu frontend
cors.init_app(app, resources={r"/*": {"origins": os.getenv("FRONTEND_ORIGIN", "https://cafe-planta-front-end-production.up.railway.app")}})

bcrypt.init_app(app)
jwt.init_app(app)

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

if __name__ == '__main__':
    app.run(debug=True)
