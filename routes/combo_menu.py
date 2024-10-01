from flask import Blueprint, jsonify
from models.base import db
from models.combo_menu import ComboMenu

combo_menu = Blueprint("combo_menu", __name__, url_prefix="/combo_menu")

@combo_menu.route("/", methods=["GET"])
def get_combo_menus():
    combos = ComboMenu.query.all()
    return jsonify([combo.serialize() for combo in combos])
