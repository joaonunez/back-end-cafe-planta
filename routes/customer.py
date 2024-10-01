from flask import Blueprint, jsonify
from models.base import db
from models.customer import Customer

customer = Blueprint("customer", __name__, url_prefix="/customer")

@customer.route("/", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.serialize() for customer in customers])
