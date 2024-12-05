from flask import Blueprint, request, jsonify
from extensions import db

from models.combo_menu_detail import combo_menu_detail
from models.combo_menu import ComboMenu
from models.product import Product

combo_menu_detail = Blueprint('combo_menu_detail', __name__, url_prefix='/combo_menu_detail')

@combo_menu_detail.route('/bulk', methods=['POST'])
def create_combo_menu_details_bulk():
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of combo_menu_detail entries"}), 400

    for detail in data:
        combo_menu_id = detail.get('combo_menu_id')
        product_id = detail.get('product_id')

        # Validar que los IDs de combo y producto existen
        if not combo_menu_id or not product_id:
            return jsonify({"error": "Missing combo_menu_id or product_id"}), 400

        combo_menu = ComboMenu.query.get(combo_menu_id)
        product = Product.query.get(product_id)

        if not combo_menu or not product:
            return jsonify({"error": f"Invalid combo_menu_id {combo_menu_id} or product_id {product_id}"}), 400

        # Asociar el producto con el combo si no está ya asociado
        if product not in combo_menu.products:
            combo_menu.products.append(product)
        else:
            return jsonify({"error": f"Product {product_id} already associated with ComboMenu {combo_menu_id}"}), 400

    db.session.commit()

    return jsonify({"message": "ComboMenu details added successfully"}), 201
