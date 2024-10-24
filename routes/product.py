from flask import Blueprint, request, jsonify
from extensions import db

from models.product import Product

product = Blueprint("product", __name__, url_prefix="/product")

@product.route("/", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])


@product.route('/bulk', methods=['POST'])
def create_products_bulk():
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of products"}), 400

    new_products = []

    for product_data in data:
        name = product_data.get('name')
        price = product_data.get('price')
        stock = product_data.get('stock')
        product_category_id = product_data.get('product_category_id')
        cafe_id = product_data.get('cafe_id')
        item_type_id = product_data.get('item_type_id')

        if not all([name, price, stock, product_category_id, cafe_id, item_type_id]):
            return jsonify({"error": "Missing required fields"}), 400

        new_product = Product(
            name=name,
            price=price,
            stock=stock,
            product_category_id=product_category_id,
            cafe_id=cafe_id,
            item_type_id=item_type_id
        )
        db.session.add(new_product)
        new_products.append(new_product)

    db.session.commit()

    return jsonify([product.serialize() for product in new_products]), 201

@product.route("/customer-request-products", methods=["GET"])
def get_customer_products():
    products = Product.query.all()
    return jsonify([product.serialize() for product in products]), 200
