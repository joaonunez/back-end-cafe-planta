from flask import Blueprint, request, jsonify
from extensions import db

from models.city import City


city = Blueprint("city", __name__, url_prefix="/city")

@city.route("/", methods=["GET"])
def get_cities():
    cities = City.query.all()
    return jsonify([city.serialize() for city in cities])

@city.route('/bulk', methods=['POST'])
def create_cities_bulk():
    data = request.get_json()
    
    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of cities"}), 400
    
    new_cities = []
    
    for city_data in data:
        name = city_data.get('name')
        state_id = city_data.get('state_id')
        
        if not name or not state_id:
            return jsonify({"error": "City name and state_id are required for all cities"}), 400
        
        new_city = City(name=name, state_id=state_id)
        db.session.add(new_city)
        new_cities.append(new_city)
    
    db.session.commit()
    
    return jsonify([city.serialize() for city in new_cities]), 201