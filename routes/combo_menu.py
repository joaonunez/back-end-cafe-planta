from flask import Blueprint, request, jsonify
from models.base import db
from models.combo_menu import ComboMenu
from models.product import Product


combo_menu = Blueprint("combo_menu", __name__, url_prefix="/combo_menu")

@combo_menu.route("/", methods=["GET"])
def get_combo_menus():
    combos = ComboMenu.query.all()
    return jsonify([combo.serialize() for combo in combos])

@combo_menu.route('/bulk', methods=['POST'])
def create_combos_bulk():
    data = request.get_json()

    # Validar que se recibe una lista de combos
    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of combos"}), 400

    new_combos = []

    for combo_data in data:
        # Extraer los campos necesarios del JSON
        name = combo_data.get('name')
        price = combo_data.get('price')
        cafe_id = combo_data.get('cafe_id')
        item_type_id = combo_data.get('item_type_id')

        # Validar que los campos requeridos estén presentes
        if not all([name, price, cafe_id, item_type_id]):
            return jsonify({"error": "Missing required fields"}), 400

        # Crear el combo sin los productos
        new_combo = ComboMenu(
            name=name,
            price=price,
            cafe_id=cafe_id,
            item_type_id=item_type_id
        )

        db.session.add(new_combo)
        new_combos.append(new_combo)

    # Confirmar los cambios en la base de datos
    db.session.commit()

    return jsonify([combo.serialize() for combo in new_combos]), 201

@combo_menu.route("/customer-request-combos", methods=["GET"])
def get_customer_combos():
    combos = ComboMenu.query.all()
    return jsonify([combo.serialize() for combo in combos]), 200
