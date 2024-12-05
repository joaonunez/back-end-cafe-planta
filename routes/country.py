from flask import Blueprint, request, jsonify
from extensions import db

from models.country import Country

country = Blueprint("country", __name__, url_prefix="/country")

@country.route("/", methods=["GET"])
def get_countries():
    countries = Country.query.all()
    return jsonify([country.serialize() for country in countries])

##crear pais
@country.route('/create-country', methods=['POST'])
def create_country():
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({"error": "Country name is required"}), 400
    
    new_country = Country(name=name)
    db.session.add(new_country)
    db.session.commit()
    
    return jsonify(new_country.serialize()), 201
