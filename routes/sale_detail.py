# sale_detail.py
from flask import Blueprint, jsonify
from models.sale_detail import SaleDetail
from models.product import Product
from models.combo_menu import ComboMenu

sale_detail = Blueprint("sale_detail", __name__, url_prefix="/sale_detail")

@sale_detail.route("/<int:sale_id>", methods=["GET"])
def get_sale_details(sale_id):
    sale_details = SaleDetail.query.filter_by(sale_id=sale_id).all()
    details_data = []

    for detail in sale_details:
        item_data = detail.serialize()
        
        if detail.item_type_id == 1:  # Producto
            product = Product.query.get(detail.item_id)
            item_data['product'] = product.serialize() if product else {}
        elif detail.item_type_id == 2:  # Combo
            combo = ComboMenu.query.get(detail.item_id)
            item_data['combo'] = combo.serialize() if combo else {}
        
        details_data.append(item_data)

    return jsonify(details_data), 200
