from flask import Blueprint, request, jsonify
from extensions import db

from models.sale_detail import SaleDetail  # Import the SaleDetail model

sale_detail = Blueprint("sale_detail", __name__, url_prefix="/sale_detail")

@sale_detail.route("/", methods=["GET"])
def get_sale_details():
    sale_details = SaleDetail.query.all()
    return jsonify([detail.serialize() for detail in sale_details])
