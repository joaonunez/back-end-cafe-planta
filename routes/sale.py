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
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

sale = Blueprint("sale", __name__, url_prefix="/sale")

# Ruta para crear una venta
@sale.route("/create", methods=["POST"])
@jwt_required()
def create_sale():
    data = request.get_json()
    customer_rut = get_jwt_identity()
    total_amount = data.get("total_amount")
    comments = data.get("comments", "")
    cart_id = data.get("cart_id")

    # Verificar la existencia del carrito
    cart = Cart.query.filter_by(id=cart_id, customer_rut=customer_rut).first()
    if not cart:
        return jsonify({"error": "Carrito no encontrado"}), 404

    # Determinar el café de los items en el carrito
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
        # Crear el objeto Sale
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

        # Crear detalles de venta
        for item in cart.items:
            unit_price = 0
            if item.item_type_id == 1:
                combo = ComboMenu.query.get(item.item_id)
                unit_price = combo.price if combo else 0
            elif item.item_type_id == 2:
                product = Product.query.get(item.item_id)
                unit_price = product.price if product else 0

            sale_detail = SaleDetail(
                sale_id=sale.id,
                quantity=item.quantity,
                unit_price=unit_price,
                item_type_id=item.item_type_id,
                item_id=item.item_id
            )
            db.session.add(sale_detail)

        # Limpiar el carrito
        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()

        return jsonify(sale.serialize()), 201
    except Exception as e:
        db.session.rollback()
        print("Error al crear la venta:", e)
        return jsonify({"error": "Error al crear la venta"}), 500

# Ruta para obtener pedidos en progreso
@sale.route("/in_progress", methods=["GET"])
@jwt_required()
def get_orders_in_progress():
    try:
        orders = Sale.query.filter_by(status="En preparación").all()
        orders_data = [order.serialize() for order in orders]
        return jsonify(orders_data), 200
    except Exception as e:
        print("Error al obtener pedidos en progreso:", e)
        return jsonify({"error": "Error al obtener pedidos en progreso"}), 500

# Ruta para que el vendedor tome una orden
@sale.route("/take_order/<int:order_id>", methods=["PUT"])
@jwt_required()
def take_order(order_id):
    waiter_rut = get_jwt_identity()
    sale = Sale.query.get(order_id)

    if sale is None or sale.status != "En preparación":
        return jsonify({"error": "La orden ya ha sido tomada o no existe"}), 400

    sale.waiter_rut = waiter_rut
    sale.status = "Orden Tomada"
    db.session.commit()

    return jsonify(sale.serialize()), 200

# Ruta para obtener las órdenes tomadas por un vendedor específico
@sale.route("/taken_orders/<string:waiter_rut>", methods=["GET"])
@jwt_required()
def get_taken_orders(waiter_rut):
    orders = Sale.query.filter_by(waiter_rut=waiter_rut, status="Orden Tomada").all()
    return jsonify([order.serialize() for order in orders]), 200

# Ruta para obtener la última venta de un cliente
@sale.route("/latest", methods=["GET"])
@jwt_required()
def get_latest_sale():
    customer_rut = get_jwt_identity()
    sale = Sale.query.filter_by(customer_rut=customer_rut).order_by(Sale.date.desc()).first()

    if not sale:
        return jsonify({"error": "No se encontró ninguna venta"}), 404

    sale_data = sale.serialize()
    sale_data["items"] = [item.serialize() for item in sale.details]

    return jsonify(sale_data), 200

# Ruta para obtener los detalles de una venta específica
@sale.route("/order_details/<int:sale_id>", methods=["GET"])
@jwt_required()
def get_order_details(sale_id):
    customer_rut = get_jwt_identity()
    sale = Sale.query.filter_by(id=sale_id, customer_rut=customer_rut).first()

    if not sale:
        return jsonify({"error": "Venta no encontrada"}), 404

    items = [item.serialize() for item in sale.details]
    return jsonify({"order_id": sale.id, "items": items}), 200

# Ruta para que el administrador obtenga todas las ventas
@sale.route("/request_all_sales_by_admin", methods=["GET"])
@jwt_required()
def request_all_sales_by_admin():
    try:
        sales = Sale.query.all()
        sales_data = [sale.serialize() for sale in sales]
        return jsonify(sales_data), 200
    except Exception as e:
        print("Error al obtener todas las ventas:", e)
        return jsonify({"error": "Error al obtener todas las ventas"}), 500

# Ruta para obtener detalles de edición de una venta específica
@sale.route("/<int:sale_id>/edit-details", methods=["GET"])
@jwt_required()
def get_sale_edit_details(sale_id):
    try:
        sale = Sale.query.get(sale_id)
        if not sale:
            return jsonify({"error": "Venta no encontrada"}), 404

        # Obtener listas de waiters, cafes, y dining areas para la edición
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
        print("Error al obtener datos de edición de venta:", e)
        return jsonify({"error": "Error al obtener datos"}), 500

# Ruta para actualizar los detalles de una venta
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

    # Cambiar estado si se asigna un mesero
    if sale.waiter_rut:
        sale.status = "Orden Tomada"
    else:
        sale.status = "En preparación"

    db.session.commit()
    return jsonify(sale.serialize()), 200

# Ruta para marcar una orden como entregada
@sale.route("/mark_as_delivered/<int:order_id>", methods=["PUT"])
@jwt_required()
def mark_as_delivered(order_id):
    sale = Sale.query.get(order_id)

    if sale is None or sale.status != "Orden Tomada":
        return jsonify({"error": "La orden no se puede marcar como entregada"}), 400

    sale.status = "Entregado"
    db.session.commit()

    return jsonify(sale.serialize()), 200

# Ruta para obtener ventas realizadas (entregadas) por un vendedor específico
@sale.route("/completed_orders/<string:waiter_rut>", methods=["GET"])
@jwt_required()
def get_completed_orders(waiter_rut):
    orders = Sale.query.filter_by(waiter_rut=waiter_rut, status="Entregado").all()
    return jsonify([order.serialize() for order in orders]), 200

@sale.route("/delete_sale_by_admin/<int:sale_id>", methods=["DELETE"])
@jwt_required()
def delete_sale_by_admin(sale_id):
    """Elimina una venta específica por el administrador."""
    try:
        # Log inicial
        print(f"Solicitud para eliminar venta con ID: {sale_id}")

        # Buscar la venta
        sale = Sale.query.get(sale_id)
        if not sale:
            print(f"Venta con ID {sale_id} no encontrada.")
            return jsonify({"error": "Venta no encontrada"}), 404

        # Eliminar los detalles de la venta
        print(f"Eliminando detalles de la venta con ID {sale_id}")
        SaleDetail.query.filter_by(sale_id=sale_id).delete()

        # Eliminar la venta
        db.session.delete(sale)
        db.session.commit()

        print(f"Venta con ID {sale_id} eliminada exitosamente.")
        return jsonify({"message": "Venta eliminada exitosamente"}), 200

    except Exception as e:
        print(f"Error al eliminar la venta: {str(e)}")
        return jsonify({"error": "Error al eliminar la venta", "details": str(e)}), 500
