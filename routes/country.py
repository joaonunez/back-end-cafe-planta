from flask import Blueprint, jsonify
from models.base import db
from models.country import Country

country = Blueprint("country", __name__, url_prefix="/country")

@country.route("/", methods=["GET"])
def get_countries():
    countries = Country.query.all()
    return jsonify([country.serialize() for country in countries])
