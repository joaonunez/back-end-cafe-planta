from flask import Blueprint, jsonify
from models.base import db
from models.product import Product

product = Blueprint("product", __name__, url_prefix="/product")

@product.route("/", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])
