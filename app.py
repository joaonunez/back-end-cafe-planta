#importacion de depéndecias
from flask import Flask, request, jsonify
from extensions import db, migrate, cors
from models import *  # Importar todos los modelos desde models/__init__.py
from routes import beneficio, cafeteria, calificacion_producto, categoria_producto, cliente, combo_menu, comuna, detalle_venta, favoritos, mesa, pais, producto, region, rol, tipo_item, usuario, venta

app = Flask(__name__)

# Configuración de base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://admin:zgVT4RIehfZuulmBOhqQLDrR9BtZPrks@dpg-crqmshrv2p9s73ea70g0-a.oregon-postgres.render.com:5432/cafeplanta"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

##para conectarse en DBeaver: jdbc:postgresql://dpg-crqmshrv2p9s73ea70g0-a.oregon-postgres.render.com:5432/cafeplanta

# Inicialización de extensiones con la aplicación Flask
db.init_app(app)
migrate.init_app(app, db)
cors.init_app(app)

# ------------------------------------
# ROUTES
# ------------------------------------
app.register_blueprint(beneficio)
app.register_blueprint(cafeteria)
app.register_blueprint(calificacion_producto)
app.register_blueprint(categoria_producto)
app.register_blueprint(cliente)
app.register_blueprint(combo_menu)
app.register_blueprint(comuna)
app.register_blueprint(detalle_venta)
app.register_blueprint(favoritos)
app.register_blueprint(mesa)
app.register_blueprint(pais)
app.register_blueprint(producto)
app.register_blueprint(region)
app.register_blueprint(rol)
app.register_blueprint(tipo_item)
app.register_blueprint(usuario)
app.register_blueprint(venta)

if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=3001, debug=True)
