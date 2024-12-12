from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from sqlalchemy.exc import IntegrityError, OperationalError
from threading import Lock
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

sale = Blueprint("sale", __name__, url_prefix="/sale")
sale_lock = Lock()


@sale.route("/create", methods=["POST"])
@jwt_required()
def create_sale():
    try:
        data = request.get_json()
        customer_rut = get_jwt_identity()
        total_amount = data.get("total_amount")
        comments = data.get("comments", "")
        cart_id = data.get("cart_id")
        dining_area_id = data.get("dining_area_id")

        if not dining_area_id:
            return jsonify({"error": "El ID de la mesa es requerido"}), 400

        dining_area = DiningArea.query.get(dining_area_id)
        if not dining_area:
            return jsonify({"error": "Mesa no encontrada"}), 404

        cafe_id = dining_area.cafe_id

        latest_sale = Sale.query.filter_by(customer_rut=customer_rut).order_by(Sale.date.desc()).first()
        if latest_sale and latest_sale.status != "Entregado":
            return jsonify({"error": "No puedes realizar un nuevo pedido mientras tu último pedido no haya sido entregado."}), 403

        cart = Cart.query.filter_by(id=cart_id, customer_rut=customer_rut).first()
        if not cart:
            return jsonify({"error": "Carrito no encontrado"}), 404

        cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
        if not cart_items:
            return jsonify({"error": "El carrito está vacío"}), 400

        sale = Sale(date=datetime.now(), total_amount=total_amount, status="En preparación", comments=comments, customer_rut=customer_rut, cafe_id=cafe_id, dining_area_id=dining_area_id)
        db.session.add(sale)
        db.session.flush()

        for item in cart_items:
            unit_price = Product.query.get(item.item_id).price if item.item_type_id == 1 else ComboMenu.query.get(item.item_id).price
            sale_detail = SaleDetail(sale_id=sale.id, quantity=item.quantity, unit_price=unit_price, item_type_id=item.item_type_id, item_id=item.item_id)
            db.session.add(sale_detail)

        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()

        return jsonify(sale.serialize()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al crear la venta", "details": str(e)}), 500


@sale.route("/in_progress", methods=["GET"])
@jwt_required()
def get_orders_in_progress():
    try:
        orders = Sale.query.filter_by(status="En preparación").all()
        return jsonify([order.serialize() for order in orders]), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener pedidos en progreso", "details": str(e)}), 500


@sale.route("/take_order/<int:order_id>", methods=["PUT"])
@jwt_required()
def take_order(order_id):
    try:
        waiter_rut = get_jwt_identity()
        sale = Sale.query.get(order_id)

        if not sale or sale.status != "En preparación":
            return jsonify({"error": "La orden ya ha sido tomada o no existe"}), 400

        sale.waiter_rut = waiter_rut
        sale.status = "Orden Tomada"
        db.session.commit()

        return jsonify(sale.serialize()), 200
    except Exception as e:
        return jsonify({"error": "Error al tomar la orden", "details": str(e)}), 500


@sale.route("/taken_orders/<string:waiter_rut>", methods=["GET"])
@jwt_required()
def get_taken_orders(waiter_rut):
    try:
        orders = Sale.query.filter_by(waiter_rut=waiter_rut, status="Orden Tomada").all()
        return jsonify([order.serialize() for order in orders]), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener órdenes tomadas", "details": str(e)}), 500


@sale.route("/latest", methods=["GET"])
@jwt_required()
def get_latest_sale():
    try:
        customer_rut = get_jwt_identity()
        sale = Sale.query.filter_by(customer_rut=customer_rut).order_by(Sale.date.desc()).first()

        if not sale:
            return jsonify({"error": "No se encontró ninguna venta"}), 404

        items = [{
            "id": detail.id,
            "name": Product.query.get(detail.item_id).name if detail.item_type_id == 1 else ComboMenu.query.get(detail.item_id).name,
            "image_url": Product.query.get(detail.item_id).image_url if detail.item_type_id == 1 else ComboMenu.query.get(detail.item_id).image_url,
            "quantity": detail.quantity,
            "unit_price": detail.unit_price,
            "total_price": detail.quantity * detail.unit_price
        } for detail in sale.details]

        sale_data = sale.serialize()
        sale_data["items"] = items

        return jsonify(sale_data), 200
    except Exception as e:
        return jsonify({"error": "Error al obtener la última venta", "details": str(e)}), 500
