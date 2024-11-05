from flask import Blueprint, request, jsonify
from extensions import db

from models.product_category import ProductCategory

product_category = Blueprint("product_category", __name__, url_prefix="/product_category")



@product_category.route('/bulk', methods=['POST'])
def create_product_categories_bulk():
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of product categories"}), 400

    new_categories = []

    for category_data in data:
        name = category_data.get('name')

        if not name:
            return jsonify({"error": "Missing 'name' field"}), 400

        new_category = ProductCategory(name=name)
        db.session.add(new_category)
        new_categories.append(new_category)

    db.session.commit()

    return jsonify([category.serialize() for category in new_categories]), 201

@product_category.route("/", methods=["GET"])
def get_product_categories():
    categories = ProductCategory.query.all()
    return jsonify([category.serialize() for category in categories])