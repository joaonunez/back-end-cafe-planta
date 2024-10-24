from flask import Blueprint, jsonify
from extensions import db

from models.product_rating import ProductRating

product_rating = Blueprint("product_rating", __name__, url_prefix="/product_rating")

@product_rating.route("/", methods=["GET"])
def get_product_ratings():
    product_ratings = ProductRating.query.all()
    return jsonify([rating.serialize() for rating in product_ratings])
