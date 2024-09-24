#importacion de depéndecias
from flask import Flask, request, jsonify
from models import db
from flask_migrate import Migrate
from flask_cors import CORS

#importacion de rutas:
from routes.beneficio import beneficio
from routes.cafeteria import cafeteria
from routes.calificacion_producto import calificacion_producto
from routes.categoria_producto import categoria_producto
from routes.cliente import cliente
from routes.combo_menu import combo_menu
from routes.comuna import comuna
from routes.detalle_venta import detalle_venta
from routes.favoritos import favoritos
from routes.mesa import mesa
from routes.pais import pais
from routes.producto import producto
from routes.region import region
from routes.rol import rol
from routes.tipo_item import tipo_item

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

##CALIFICACION PRODUCTO:
app.register_blueprint(calificacion_producto)

##CATEGORIA PRODUCTO:
app.register_blueprint(categoria_producto)

##CLIENTE:
app.register_blueprint(cliente)

##COMBO MENU:
app.register_blueprint(combo_menu)

##COMUNA:
app.register_blueprint(comuna)

##DETALLE VENTA:
app.register_blueprint(detalle_venta)

##FAVORITOS:
app.register_blueprint(favoritos)

##MESA:
app.register_blueprint(mesa)

##PAIS:
app.register_blueprint(pais)

##PRODUCTO:
app.register_blueprint(producto)

##REGION:
app.register_blueprint(region)

##ROL:
app.register_blueprint(rol)

##TIPO ITEM:
app.register_blueprint(tipo_item)

##USUARIO:
app.register_blueprint(usuario)

##VENTA:
app.register_blueprint(venta)


if  __name__ == "__main__": 
    app.run(host= "0.0.0.0", port= 3001, debug= True)