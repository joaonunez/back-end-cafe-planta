from flask import Blueprint, request, jsonify
from models.base import db
from models.benefit import Benefit

benefit = Blueprint("benefit", __name__, url_prefix="/benefit")

@benefit.route("/", methods=["GET"])
def get_benefits():
    benefits = Benefit.query.all()
    return jsonify([benefit.serialize() for benefit in benefits])

@benefit.route('/bulk', methods=['POST'])
def create_benefits_bulk():
    data = request.get_json()
    
    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of benefits"}), 400
    
    new_benefits = []
    
    for benefit_data in data:
        price = benefit_data.get('price')
        description = benefit_data.get('description')
        
        if price is None or not description:
            return jsonify({"error": "Both price and description are required for all benefits"}), 400
        
        new_benefit = Benefit(price=price, description=description)
        db.session.add(new_benefit)
        new_benefits.append(new_benefit)
    
    db.session.commit()
    
    return jsonify([benefit.serialize() for benefit in new_benefits]), 201