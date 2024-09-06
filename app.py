import os
from flask import Flask, request, jsonify
from models import db, Pais, Region, Comuna, Rol, Beneficio, User, Producto, CategoriaProducto, ComboMenu, Cafeteria, TipoItem, Venta, DetalleVenta
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafeteria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

@app.route('/')
def home():
    return "<h1>Cafetería API</h1>"

# CRUD para Pais
@app.route('/pais', methods=['POST'])
def create_pais():
    data = request.get_json()
    pais = Pais(**data)
    db.session.add(pais)
    db.session.commit()
    return jsonify(pais.serialize()), 201

@app.route('/pais/<int:id>', methods=['GET'])
def get_pais(id):
    pais = Pais.query.get(id)
    return jsonify(pais.serialize()), 200 if pais else 404

@app.route('/pais/<int:id>', methods=['PUT'])
def update_pais(id):
    pais = Pais.query.get(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(pais, key, value)
    db.session.commit()
    return jsonify(pais.serialize()), 200

@app.route('/pais/<int:id>', methods=['DELETE'])
def delete_pais(id):
    pais = Pais.query.get(id)
    db.session.delete(pais)
    db.session.commit()
    return jsonify({'message': 'Pais deleted'}), 200

# CRUD para Region
@app.route('/region', methods=['POST'])
def create_region():
    data = request.get_json()
    region = Region(**data)
    db.session.add(region)
    db.session.commit()
    return jsonify(region.serialize()), 201

@app.route('/region/<int:id>', methods=['GET'])
def get_region(id):
    region = Region.query.get(id)
    return jsonify(region.serialize()), 200 if region else 404

@app.route('/region/<int:id>', methods=['PUT'])
def update_region(id):
    region = Region.query.get(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(region, key, value)
    db.session.commit()
    return jsonify(region.serialize()), 200

@app.route('/region/<int:id>', methods=['DELETE'])
def delete_region(id):
    region = Region.query.get(id)
    db.session.delete(region)
    db.session.commit()
    return jsonify({'message': 'Region deleted'}), 200

# CRUD para Comuna
@app.route('/comuna', methods=['POST'])
def create_comuna():
    data = request.get_json()
    comuna = Comuna(**data)
    db.session.add(comuna)
    db.session.commit()
    return jsonify(comuna.serialize()), 201

@app.route('/comuna/<int:id>', methods=['GET'])
def get_comuna(id):
    comuna = Comuna.query.get(id)
    return jsonify(comuna.serialize()), 200 if comuna else 404

@app.route('/comuna/<int:id>', methods=['PUT'])
def update_comuna(id):
    comuna = Comuna.query.get(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(comuna, key, value)
    db.session.commit()
    return jsonify(comuna.serialize()), 200

@app.route('/comuna/<int:id>', methods=['DELETE'])
def delete_comuna(id):
    comuna = Comuna.query.get(id)
    db.session.delete(comuna)
    db.session.commit()
    return jsonify({'message': 'Comuna deleted'}), 200

# CRUD para Rol
@app.route('/rol', methods=['POST'])
def create_rol():
    data = request.get_json()
    rol = Rol(**data)
    db.session.add(rol)
    db.session.commit()
    return jsonify(rol.serialize()), 201

@app.route('/rol/<int:id>', methods=['GET'])
def get_rol(id):
    rol = Rol.query.get(id)
    return jsonify(rol.serialize()), 200 if rol else 404

@app.route('/rol/<int:id>', methods=['PUT'])
def update_rol(id):
    rol = Rol.query.get(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(rol, key, value)
    db.session.commit()
    return jsonify(rol.serialize()), 200

@app.route('/rol/<int:id>', methods=['DELETE'])
def delete_rol(id):
    rol = Rol.query.get(id)
    db.session.delete(rol)
    db.session.commit()
    return jsonify({'message': 'Rol deleted'}), 200

# CRUD para Beneficio
@app.route('/beneficio', methods=['POST'])
def create_beneficio():
    data = request.get_json()
    beneficio = Beneficio(**data)
    db.session.add(beneficio)
    db.session.commit()
    return jsonify(beneficio.serialize()), 201

@app.route('/beneficio/<int:id>', methods=['GET'])
def get_beneficio(id):
    beneficio = Beneficio.query.get(id)
    return jsonify(beneficio.serialize()), 200 if beneficio else 404

@app.route('/beneficio/<int:id>', methods=['PUT'])
def update_beneficio(id):
    beneficio = Beneficio.query.get(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(beneficio, key, value)
    db.session.commit()
    return jsonify(beneficio.serialize()), 200

@app.route('/beneficio/<int:id>', methods=['DELETE'])
def delete_beneficio(id):
    beneficio = Beneficio.query.get(id)
    db.session.delete(beneficio)
    db.session.commit()
    return jsonify({'message': 'Beneficio deleted'}), 200

# CRUD para User
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return jsonify(user.serialize()), 200 if user else 404

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify(user.serialize()), 200

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

# CRUD para Producto
@app.route('/producto', methods=['POST'])
def create_producto():
    data = request.get_json()
    producto = Producto(**data)
    db.session.add(producto)
    db.session.commit()
    return jsonify(producto.serialize()), 201

@app.route('/producto/<int:id>', methods=['GET'])
def get_producto(id):
    producto = Producto.query.get(id)
    return jsonify(producto.serialize()), 200 if producto else 404

@app.route('/producto/<int:id>', methods=['PUT'])
def update_producto(id):
    producto = Producto.query.get(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(producto, key, value)
    db.session.commit()
    return jsonify(producto.serialize()), 200

@app.route('/producto/<int:id>', methods=['DELETE'])
def delete_producto(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return jsonify({'message': 'Producto deleted'}), 200

# CRUD para CategoriaProducto
@app.route('/categoria_producto', methods=['POST'])
def create_categoria_producto():
    data = request.get_json()
    categoria = CategoriaProducto(**data)
    db.session.add(categoria)
    db.session.commit()
    return jsonify(categoria.serialize()), 201

@app.route('/categoria_producto/<int:id>', methods=['GET'])
def get_categoria_producto(id):
    categoria = CategoriaProducto.query.get(id)
    return jsonify(categoria.serialize()), 200 if categoria else 404

@app.route('/categoria_producto/<int:id>', methods=['PUT'])
def update_categoria_producto(id):
    categoria = CategoriaProducto.query.get(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(categoria, key, value)
    db.session.commit()
    return jsonify(categoria.serialize()), 200

@app.route('/categoria_producto/<int:id>', methods=['DELETE'])
def delete_categoria_producto(id):
    categoria = CategoriaProducto.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({'message': 'CategoriaProducto deleted'}), 200

# CRUD para ComboMenu
@app.route('/combo_menu', methods=['POST'])
def create_combo_menu():
    data = request.get_json()
    combo = ComboMenu(**data)
    db.session.add(combo)
    db.session.commit()
    return jsonify(combo.serialize()), 201

@app.route('/combo_menu/<int:id>', methods=['GET'])
def get_combo_menu(id):
    combo = ComboMenu.query.get(id)
    return jsonify(combo.serialize()), 200 if combo else 404

@app.route('/combo_menu/<int:id>', methods=['PUT'])
def update_combo_menu(id):
    combo = ComboMenu.query.get(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(combo, key, value)
    db.session.commit()
    return jsonify(combo.serialize()), 200

@app.route('/combo_menu/<int:id>', methods=['DELETE'])
def delete_combo_menu(id):
    combo = ComboMenu.query.get(id)
    db.session.delete(combo)
    db.session.commit()
    return jsonify({'message': 'ComboMenu deleted'}), 200

# CRUD para Cafeteria
@app.route('/cafeteria', methods=['POST'])
def create_cafeteria():
    data = request.get_json()
    cafeteria = Cafeteria(**data)
    db.session.add(cafeteria)
    db.session.commit()
    return jsonify(cafeteria.serialize()), 201

@app.route('/cafeteria/<int:id>', methods=['GET'])
def get_cafeteria(id):
    cafeteria = Cafeteria.query.get(id)
    return jsonify(cafeteria.serialize()), 200 if cafeteria else 404

@app.route('/cafeteria/<int:id>', methods=['PUT'])
def update_cafeteria(id):
    cafeteria = Cafeteria.query.get(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(cafeteria, key, value)
    db.session.commit()
    return jsonify(cafeteria.serialize()), 200

@app.route('/cafeteria/<int:id>', methods=['DELETE'])
def delete_cafeteria(id):
    cafeteria = Cafeteria.query.get(id)
    db.session.delete(cafeteria)
    db.session.commit()
    return jsonify({'message': 'Cafeteria deleted'}), 200

# CRUD para TipoItem
@app.route('/tipo_item', methods=['POST'])
def create_tipo_item():
    data = request.get_json()
    tipo_item = TipoItem(**data)
    db.session.add(tipo_item)
    db.session.commit()
    return jsonify(tipo_item.serialize()), 201

@app.route('/tipo_item/<int:id>', methods=['GET'])
def get_tipo_item(id):
    tipo_item = TipoItem.query.get(id)
    return jsonify(tipo_item.serialize()), 200 if tipo_item else 404

@app.route('/tipo_item/<int:id>', methods=['PUT'])
def update_tipo_item(id):
    tipo_item = TipoItem.query.get(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(tipo_item, key, value)
    db.session.commit()
    return jsonify(tipo_item.serialize()), 200

@app.route('/tipo_item/<int:id>', methods=['DELETE'])
def delete_tipo_item(id):
    tipo_item = TipoItem.query.get(id)
    db.session.delete(tipo_item)
    db.session.commit()
    return jsonify({'message': 'TipoItem deleted'}), 200

# CRUD para Venta
@app.route('/venta', methods=['POST'])
def create_venta():
    data = request.get_json()
    venta = Venta(**data)
    db.session.add(venta)
    db.session.commit()
    return jsonify(venta.serialize()), 201

@app.route('/venta/<int:id>', methods=['GET'])
def get_venta(id):
    venta = Venta.query.get(id)
    return jsonify(venta.serialize()), 200 if venta else 404

@app.route('/venta/<int:id>', methods=['PUT'])
def update_venta(id):
    venta = Venta.query.get(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(venta, key, value)
    db.session.commit()
    return jsonify(venta.serialize()), 200

@app.route('/venta/<int:id>', methods=['DELETE'])
def delete_venta(id):
    venta = Venta.query.get(id)
    db.session.delete(venta)
    db.session.commit()
    return jsonify({'message': 'Venta deleted'}), 200

# CRUD para DetalleVenta
@app.route('/detalle_venta', methods=['POST'])
def create_detalle_venta():
    data = request.get_json()
    detalle_venta = DetalleVenta(**data)
    db.session.add(detalle_venta)
    db.session.commit()
    return jsonify(detalle_venta.serialize()), 201

@app.route('/detalle_venta/<int:id>', methods=['GET'])
def get_detalle_venta(id):
    detalle_venta = DetalleVenta.query.get(id)
    return jsonify(detalle_venta.serialize()), 200 if detalle_venta else 404

@app.route('/detalle_venta/<int:id>', methods=['PUT'])
def update_detalle_venta(id):
    detalle_venta = DetalleVenta.query.get(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(detalle_venta, key, value)
    db.session.commit()
    return jsonify(detalle_venta.serialize()), 200

@app.route('/detalle_venta/<int:id>', methods=['DELETE'])
def delete_detalle_venta(id):
    detalle_venta = DetalleVenta.query.get(id)
    db.session.delete(detalle_venta)
    db.session.commit()
    return jsonify({'message': 'DetalleVenta deleted'}), 200

# Ejecución del servidor local
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
