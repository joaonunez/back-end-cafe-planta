from flask import Blueprint, jsonify
from models import ComboMenu
from models import db

combo_menu = Blueprint("combo_menu", __name__, url_prefix="/camping")

@combo_menu.route("/combo_menu", methods=["GET"])
def get_combo_menus():
    combos = ComboMenu.query.all()
    return jsonify([combo.serializar() for combo in combos])
