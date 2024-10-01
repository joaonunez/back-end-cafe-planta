from flask import Blueprint, jsonify
from models.base import db
from models.city import City

city = Blueprint("city", __name__, url_prefix="/city")

@city.route("/", methods=["GET"])
def get_cities():
    cities = City.query.all()
    return jsonify([city.serialize() for city in cities])
