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
    
    data = request.get_json()
    print("Datos recibidos:", data)
    
    customer_rut = get_jwt_identity()
    print("Cliente autenticado con RUT:", customer_rut)
    
    total_amount = data.get("total_amount")
    comments = data.get("comments", "")
    cart_id = data.get("cart_id")
    print(f"Total amount: {total_amount}, Comments: {comments}, Cart ID: {cart_id}")

    cart = Cart.query.filter_by(id=cart_id, customer_rut=customer_rut).first()
    if not cart:
        print(f"Error: Carrito no encontrado para Cart ID: {cart_id} y RUT: {customer_rut}")
        return jsonify({"error": "Carrito no encontrado"}), 404
    print(f"Carrito encontrado: {cart.serialize()}")

    cafe_id = None
    for item in cart.items:
        print(f"Procesando item en carrito para determinar cafe_id: {item.serialize()}")
        if item.item_type_id == 1:
            combo = ComboMenu.query.get(item.item_id)
            if combo:
                cafe_id = combo.cafe_id
        elif item.item_type_id == 2:
            product = Product.query.get(item.item_id)
            if product:
                cafe_id = product.cafe_id
        if cafe_id:
            print(f"cafe_id determinado: {cafe_id}")
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
        print(f"Venta creada con ID: {sale.id}")
    except Exception as e:
        print("Error al crear la venta:", e)
        return jsonify({"error": "Error al crear la venta"}), 500

    try:
        for item in cart.items:
            print(f"Procesando item del carrito: {item.serialize()}")
            if item.item_type_id == 1:
                combo = ComboMenu.query.get(item.item_id)
                unit_price = combo.price if combo else 0
                print(f"Item Combo encontrado: {combo.serialize() if combo else 'No encontrado'}, Precio unitario: {unit_price}")
            elif item.item_type_id == 2:
                product = Product.query.get(item.item_id)
                unit_price = product.price if product else 0
                print(f"Item Product encontrado: {product.serialize() if product else 'No encontrado'}, Precio unitario: {unit_price}")
            else:
                print("Error: item_type_id desconocido.")
                continue

            sale_detail = SaleDetail(
                sale_id=sale.id,
                quantity=item.quantity,
                unit_price=unit_price,
                item_type_id=item.item_type_id,
                item_id=item.item_id
            )
            db.session.add(sale_detail)
            print("Detalle de venta añadido:", sale_detail.serialize())
    except Exception as e:
        print("Error al procesar los detalles de venta:", e)
        db.session.rollback()
        return jsonify({"error": "Error al crear detalles de venta"}), 500

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

@sale.route("/order_details/<int:sale_id>", methods=["GET"])
@jwt_required()
def get_order_details(sale_id):
    customer_rut = get_jwt_identity()
    sale = Sale.query.filter_by(id=sale_id, customer_rut=customer_rut).first()

    if not sale:
        return jsonify({"error": "Venta no encontrada"}), 404

    items = []
    for detail in sale.details:
        item_data = {
            "quantity": detail.quantity,
            "unit_price": detail.unit_price,
            "item_type_id": detail.item_type_id,
            "item_id": detail.item_id
        }
        
        if detail.item_type_id == 1:
            combo = ComboMenu.query.get(detail.item_id)
            if combo:
                item_data.update({
                    "name": combo.name,
                    "image_url": combo.image_url
                })
        elif detail.item_type_id == 2:
            product = Product.query.get(detail.item_id)
            if product:
                item_data.update({
                    "name": product.name,
                    "image_url": product.image_url
                })

        items.append(item_data)

    return jsonify({"order_id": sale.id, "items": items}), 200
