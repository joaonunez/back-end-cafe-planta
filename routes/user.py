from flask import Blueprint, jsonify
from models.base import db
from models.user import User

user = Blueprint("user", __name__, url_prefix="/user")

@user.route("/", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])
