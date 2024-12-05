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

@sale.route("/create", methods=["POST"])
@jwt_required()
def create_sale():
    """Crea una venta, incluyendo los detalles del carrito como SaleDetail."""
    try:
        data = request.get_json()
        customer_rut = get_jwt_identity()
        total_amount = data.get("total_amount")
        comments = data.get("comments", "")
        cart_id = data.get("cart_id")
        dining_area_id = data.get("dining_area_id")

        if not dining_area_id:
            return jsonify({"error": "El ID de la mesa es requerido"}), 400

        # Verificar el estado del último pedido
        latest_sale = Sale.query.filter_by(customer_rut=customer_rut).order_by(Sale.date.desc()).first()
        if latest_sale and latest_sale.status != "Entregado":
            return jsonify({
                "error": "No puedes realizar un nuevo pedido mientras tu último pedido no haya sido entregado."
            }), 403

        # Verificar existencia de la mesa
        dining_area = DiningArea.query.get(dining_area_id)
        if not dining_area:
            return jsonify({"error": "Mesa no encontrada"}), 404

        cafe_id = dining_area.cafe_id

        # Validar existencia del carrito
        cart = Cart.query.filter_by(id=cart_id, customer_rut=customer_rut).first()
        if not cart:
            return jsonify({"error": "Carrito no encontrado"}), 404

        # Crear la venta
        sale = Sale(
            date=datetime.now(),
            total_amount=total_amount,
            status="En preparación",
            comments=comments,
            customer_rut=customer_rut,
            cafe_id=cafe_id,
            dining_area_id=dining_area_id,
        )
        db.session.add(sale)
        db.session.flush()  # Obtener el ID de la venta

        # Agregar detalles desde el carrito
        cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
        if not cart_items:
            return jsonify({"error": "El carrito está vacío"}), 400

        for item in cart_items:
            # Obtener precio según el tipo de item
            if item.item_type_id == 1:  # Producto
                product = Product.query.get(item.item_id)
                unit_price = product.price if product else 0
            elif item.item_type_id == 2:  # Combo
                combo = ComboMenu.query.get(item.item_id)
                unit_price = combo.price if combo else 0

            sale_detail = SaleDetail(
                sale_id=sale.id,
                quantity=item.quantity,
                unit_price=unit_price,
                item_type_id=item.item_type_id,
                item_id=item.item_id,
            )
            db.session.add(sale_detail)

        # Vaciar el carrito
        CartItem.query.filter_by(cart_id=cart.id).delete()

        db.session.commit()

        return jsonify(sale.serialize()), 201

    except Exception as e:
        print(f"Error al crear venta: {e}")
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

    # Resolver detalles con datos de productos o combos
    items = []
    for detail in sale.details:
        if detail.item_type_id == 1:  # Combo
            combo = ComboMenu.query.get(detail.item_id)
            if combo:
                items.append({
                    "id": detail.id,
                    "name": combo.name,
                    "image_url": combo.image_url,
                    "quantity": detail.quantity,
                    "unit_price": detail.unit_price,
                    "total_price": detail.quantity * detail.unit_price
                })
        elif detail.item_type_id == 2:  # Producto
            product = Product.query.get(detail.item_id)
            if product:
                items.append({
                    "id": detail.id,
                    "name": product.name,
                    "image_url": product.image_url,
                    "quantity": detail.quantity,
                    "unit_price": detail.unit_price,
                    "total_price": detail.quantity * detail.unit_price
                })

    sale_data = sale.serialize()
    sale_data["items"] = items

    return jsonify(sale_data), 200


@sale.route("/order_details/<int:sale_id>", methods=["GET"])
@jwt_required()
def get_order_details(sale_id):
    sale = Sale.query.get(sale_id)

    if not sale:
        return jsonify({"error": "Venta no encontrada"}), 404

    items = []
    for detail in sale.details:
        if detail.item_type_id == 1:  # Combo
            combo = ComboMenu.query.get(detail.item_id)
            if combo:
                items.append({
                    "id": detail.id,
                    "name": combo.name,
                    "image_url": combo.image_url,
                    "quantity": detail.quantity,
                    "unit_price": detail.unit_price,
                    "total_price": detail.quantity * detail.unit_price,
                })
        elif detail.item_type_id == 2:  # Producto
            product = Product.query.get(detail.item_id)
            if product:
                items.append({
                    "id": detail.id,
                    "name": product.name,
                    "image_url": product.image_url,
                    "quantity": detail.quantity,
                    "unit_price": detail.unit_price,
                    "total_price": detail.quantity * detail.unit_price,
                })

    return jsonify({"order_id": sale.id, "items": items, "date": sale.date, "comments": sale.comments}), 200



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

@sale.route("/purchase_history", methods=["GET"])
@jwt_required()
def get_purchase_history():
    customer_rut = get_jwt_identity()
    try:
        # Obtener todas las ventas de un cliente, ordenadas por fecha
        sales = Sale.query.filter_by(customer_rut=customer_rut).order_by(Sale.date.desc()).all()

        if not sales:
            return jsonify({"error": "No se encontraron ventas"}), 404

        # Serializar ventas excluyendo la última
        all_sales = []
        for sale in sales[1:]:  # Excluir la última venta
            serialized_sale = sale.serialize()
            serialized_sale["items"] = [
                detail.serialize() for detail in sale.details
            ]  # Añadir detalles de los ítems
            all_sales.append(serialized_sale)

        return jsonify(all_sales), 200

    except Exception as e:
        print("Error al obtener el historial de compras:", e)
        return jsonify({"error": "Error al obtener el historial de compras"}), 500


# Ruta para verificar el estado del último pedido
@sale.route("/validate_latest_order", methods=["GET"])
@jwt_required()
def validate_latest_order():
    customer_rut = get_jwt_identity()
    try:
        latest_sale = Sale.query.filter_by(customer_rut=customer_rut).order_by(Sale.date.desc()).first()
        if not latest_sale:
            return jsonify({"can_create_order": True})  # Si no hay ventas, puede realizar un pedido
        
        if latest_sale.status != "Entregado":
            return jsonify({
                "can_create_order": False,
                "message": "No puedes realizar un nuevo pedido mientras tu último pedido no haya sido entregado."
            }), 403

        return jsonify({"can_create_order": True}), 200
    except Exception as e:
        print("Error al validar el último pedido:", e)
        return jsonify({"error": "Error al validar el último pedido"}), 500
