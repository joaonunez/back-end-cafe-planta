import os
from flask import Flask, request, jsonify
from werkzeug.exceptions import Unauthorized
from extensions import db, migrate, cors, bcrypt, jwt
from models import *  # Importar todos los modelos desde models/__init__.py
from routes import (
    benefit, benefit_user, cafe, cart, product_rating, 
    product_category, customer, combo_menu, combo_menu_detail, 
    city, sale_detail, favorite, dining_area, country, 
    product, state, role, item_type, user, sale, cloudinary_bp
)
import cloudinary

# ------------------------------------
# FACTORY DE CREACIÓN DE FLASK APP
# ------------------------------------
def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicialización de extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Configuración Cloudinary
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET")
    )

    # Manejo de errores
    @app.errorhandler(Unauthorized)
    def handle_unauthorized(e):
        return jsonify({"error": "Invalid or expired token"}), 401

    @app.errorhandler(Exception)
    def handle_exception(e):
        print(f"Error inesperado: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

    # Registro de rutas
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

# Requerido por Vercel
app = create_app()

# Este "handler" es requerido para la integración con Vercel
def handler(event, context):
    from mangum import Mangum
    asgi_app = app
    return Mangum(asgi_app)(event, context)
