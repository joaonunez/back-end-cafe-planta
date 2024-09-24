#importacion de depéndecias
from flask import Flask, request, jsonify
from models import db
from flask_migrate import Migrate
from flask_cors import CORS

#importacion de rutas:
from routes.beneficio import beneficio
from routes.cafeteria import cafeteria
from routes.categoria_producto import categoria_producto
from routes.combo_menu import combo_menu
from routes.comuna import comuna
from routes.detalle_venta import detalle_venta
from routes.pais import pais
from routes.producto import producto
from routes.region import region
from routes.rol import rol
from routes.tipo_item import tipo_item
from routes.usuario

app = Flask(__name__)

#configuracion de base de datos:
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://cafe_planta_user:X94KTKqoqHlkfhE7s588ainlCB9zBCQY@dpgcrp9ir2j1k6c73c28b50-a.oregon-postgres.render.com/cafe_planta"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Inicialización de la base de datos y migración
db.init_app(app)
Migrate(app, db)

# Habilitar CORS
CORS(app)

# ------------------------------------
# ROUTES
# ------------------------------------
##BENEFICIO:
app.register_blueprint(beneficio)
##CAFETERIA:
app.register_blueprint(cafeteria)
##


if  __name__ == "__main__": 
    app.run(host= "0.0.0.0", port= 3001, debug= True)