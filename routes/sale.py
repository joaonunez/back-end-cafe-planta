from flask import Blueprint, request, jsonify
from extensions import db
from models.sale import Sale
from models.sale_detail import SaleDetail
from models.cart import Cart
from models.cart_item import CartItem
from models.product import Product
from models.combo_menu import ComboMenu
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

sale = Blueprint("sale", __name__, url_prefix="/sale")

@sale.route("/create", methods=["POST"])
@jwt_required()
def create_sale():
    print("Iniciando la creación de la venta...")
    
    # Verifica la carga de datos y el JWT
    data = request.get_json()
    print("Datos recibidos:", data)
    
    customer_rut = get_jwt_identity()
    print("Cliente autenticado con RUT:", customer_rut)
    
    total_amount = data.get("total_amount")
    comments = data.get("comments", "")
    cart_id = data.get("cart_id")
    print(f"Total amount: {total_amount}, Comments: {comments}, Cart ID: {cart_id}")

    # Validación y obtención del carrito
    cart = Cart.query.filter_by(id=cart_id, customer_rut=customer_rut).first()
    if not cart:
        print(f"Error: Carrito no encontrado para Cart ID: {cart_id} y RUT: {customer_rut}")
        return jsonify({"error": "Carrito no encontrado"}), 404
    print(f"Carrito encontrado: {cart.serialize()}")

    # Creación de la venta
    try:
        sale = Sale(
            date=datetime.now(),
            total_amount=total_amount,
            status="En preparación",
            comments=comments,
            customer_rut=customer_rut,
            cafe_id=cart.items[0].item.cafe_id if cart.items else None
        )
        db.session.add(sale)
        db.session.flush()  # Para obtener el ID de la venta
        print(f"Venta creada con ID: {sale.id}")
    except Exception as e:
        print("Error al crear la venta:", e)
        return jsonify({"error": "Error al crear la venta"}), 500

    # Creación de los detalles de venta
    try:
        for item in cart.items:
            print(f"Procesando item del carrito: {item.serialize()}")
            sale_detail = SaleDetail(
                sale_id=sale.id,
                quantity=item.quantity,
                unit_price=item.item.price,
                item_type_id=item.item_type_id,
                item_id=item.item_id
            )
            db.session.add(sale_detail)
            print("Detalle de venta añadido:", sale_detail.serialize())
    except Exception as e:
        print("Error al procesar los detalles de venta:", e)
        db.session.rollback()
        return jsonify({"error": "Error al crear detalles de venta"}), 500

    # Eliminación de los elementos del carrito
    try:
        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()
        print("Items del carrito eliminados y transacción de venta completada")
    except Exception as e:
        print("Error al eliminar los elementos del carrito:", e)
        db.session.rollback()
        return jsonify({"error": "Error al vaciar el carrito"}), 500

    return jsonify(sale.serialize()), 201

@sale.route("/latest", methods=["GET"])
@jwt_required()
def get_latest_sale():
    customer_rut = get_jwt_identity()
    print(f"Buscando la última venta para el cliente con RUT: {customer_rut}")
    
    sale = Sale.query.filter_by(customer_rut=customer_rut).order_by(Sale.date.desc()).first()
    if not sale:
        print("No se encontró ninguna venta para el cliente.")
        return jsonify({"error": "No se encontró ninguna venta para este cliente."}), 404

    print(f"Última venta encontrada: {sale.serialize()}")
    sale_data = sale.serialize()
    sale_data["items"] = [item.serialize() for item in sale.details]
    
    return jsonify(sale_data), 200
