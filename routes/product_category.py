from flask import Blueprint, jsonify
from models.base import db
from models.product_category import ProductCategory

product_category = Blueprint("product_category", __name__, url_prefix="/product_category")

@product_category.route("/", methods=["GET"])
def get_product_categories():
    categories = ProductCategory.query.all()
    return jsonify([category.serialize() for category in categories])
