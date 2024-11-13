from flask import Blueprint, request, jsonify
from extensions import db
from models.sale import Sale
from models.sale_detail import SaleDetail
from models.cart import Cart
from models.cart_item import CartItem
from models.product import Product
from models.combo_menu import ComboMenu
from models.user import User
from models.cafe import Cafe
from models.dining_area import DiningArea
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

sale = Blueprint("sale", __name__, url_prefix="/sale")

# Crear una venta
@sale.route("/create", methods=["POST"])
@jwt_required()
def create_sale():
    data = request.get_json()
    customer_rut = get_jwt_identity()

    total_amount = data.get("total_amount")
    comments = data.get("comments", "")
    cart_id = data.get("cart_id")

    cart = Cart.query.filter_by(id=cart_id, customer_rut=customer_rut).first()
    if not cart:
        return jsonify({"error": "Carrito no encontrado"}), 404

    cafe_id = None
    for item in cart.items:
        if item.item_type_id == 1:
            combo = ComboMenu.query.get(item.item_id)
            if combo:
                cafe_id = combo.cafe_id
        elif item.item_type_id == 2:
            product = Product.query.get(item.item_id)
            if product:
                cafe_id = product.cafe_id
        if cafe_id:
            break

    try:
        sale = Sale(
            date=datetime.now(),
            total_amount=total_amount,
            status="En preparación",
            comments=comments,
            customer_rut=customer_rut,
            cafe_id=cafe_id
        )
        db.session.add(sale)
        db.session.flush()

        for item in cart.items:
            if item.item_type_id == 1:
                combo = ComboMenu.query.get(item.item_id)
                unit_price = combo.price if combo else 0
            elif item.item_type_id == 2:
                product = Product.query.get(item.item_id)
                unit_price = product.price if product else 0
            else:
                continue

            sale_detail = SaleDetail(
                sale_id=sale.id,
                quantity=item.quantity,
                unit_price=unit_price,
                item_type_id=item.item_type_id,
                item_id=item.item_id
            )
            db.session.add(sale_detail)

        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()

        return jsonify(sale.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al crear la venta"}), 500

# Obtener detalles para editar una venta
@sale.route("/<int:sale_id>/edit-details", methods=["GET"])
@jwt_required()
def get_sale_edit_details(sale_id):
    try:
        sale = Sale.query.get(sale_id)
        if not sale:
            return jsonify({"error": "Venta no encontrada"}), 404

        waiters = User.query.filter_by(role_id=3).all()
        cafes = Cafe.query.all()
        dining_areas = DiningArea.query.all()

        response = {
            "sale": sale.serialize(),
            "waiters": [waiter.serialize() for waiter in waiters],
            "cafes": [cafe.serialize() for cafe in cafes],
            "dining_areas": [area.serialize() for area in dining_areas],
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener datos"}), 500

# Actualizar los detalles de una venta específica
@sale.route("/<int:sale_id>/edit-details", methods=["PUT"])
@jwt_required()
def update_sale_details(sale_id):
    data = request.get_json()
    sale = Sale.query.get(sale_id)

    if not sale:
        return jsonify({"error": "Venta no encontrada"}), 404

    sale.total_amount = data.get("total_amount", sale.total_amount)
    sale.comments = data.get("comments", sale.comments)
    sale.waiter_rut = data.get("waiter_rut", sale.waiter_rut)
    sale.cafe_id = data.get("cafe_id", sale.cafe_id)
    sale.dining_area_id = data.get("dining_area_id", sale.dining_area_id)

    db.session.commit()
    return jsonify(sale.serialize()), 200

# Obtener todas las ventas sin filtrar (para administradores)
@sale.route("/request_all_sales_by_admin", methods=["GET"])
@jwt_required()
def request_all_sales_by_admin():
    try:
        sales = Sale.query.all()
        sales_data = [sale.serialize() for sale in sales]
        return jsonify(sales_data), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener todas las ventas"}), 500
