from flask import Blueprint, request, jsonify
from models.base import db  # Importar db desde base.py
from models.combo_menu import ComboMenu  # Importar el modelo ComboMenu

combo_menu = Blueprint("combo_menu", __name__, url_prefix="/camping")

@combo_menu.route("/combo_menu", methods=["GET"])
def get_combos():
    combos = ComboMenu.query.all()
    return jsonify([combo.serializar() for combo in combos])
