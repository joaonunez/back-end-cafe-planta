from flask import Blueprint, jsonify
from models.base import db
from models.favorite import Favorite

favorite = Blueprint("favorite", __name__, url_prefix="/favorite")

@favorite.route("/", methods=["GET"])
def get_favorites():
    favorites = Favorite.query.all()
    return jsonify([favorite.serialize() for favorite in favorites])
