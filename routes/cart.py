from flask import Blueprint, request, jsonify
from extensions import db
from models.cart import Cart
from models.product import Product
from models.combo_menu import ComboMenu
from models.cart_item import CartItem
from flask_jwt_extended import jwt_required, get_jwt_identity

cart = Blueprint("cart", __name__, url_prefix="/cart")

@cart.route('/add_item', methods=['POST'])
@jwt_required()
def add_to_cart():
    data = request.get_json()
    item_id = data.get("item_id")
    item_type_id = data.get("item_type_id")
    quantity = data.get("quantity", 1)

    if not item_id or not item_type_id:
        return jsonify({"error": "Item ID and Item Type ID are required"}), 400

    customer_rut = get_jwt_identity()
    cart = Cart.query.filter_by(customer_rut=customer_rut).first()
    if not cart:
        cart = Cart(customer_rut=customer_rut)
        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem.query.filter_by(cart_id=cart.id, item_id=item_id, item_type_id=item_type_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.id, item_id=item_id, item_type_id=item_type_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({"message": "Item added to cart successfully", "cart": cart.serialize()}), 200

@cart.route('/get_items', methods=['GET'])
@jwt_required()
def get_cart_items():
    customer_rut = get_jwt_identity()
    cart = Cart.query.filter_by(customer_rut=customer_rut).first()
    
    if not cart:
        return jsonify({"cart": []})

    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    items = []
    for item in cart_items:
        if item.item_type_id == 1:
            combo = ComboMenu.query.get(item.item_id)
            if combo:
                items.append({
                    "id": item.id,
                    "cart_id": item.cart_id,
                    "item_id": item.item_id,
                    "item_type_id": item.item_type_id,
                    "quantity": item.quantity,
                    "name": combo.name,
                    "price": combo.price,
                    "image_url": combo.image_url
                })
        elif item.item_type_id == 2:
            product = Product.query.get(item.item_id)
            if product:
                items.append({
                    "id": item.id,
                    "cart_id": item.cart_id,
                    "item_id": item.item_id,
                    "item_type_id": item.item_type_id,
                    "quantity": item.quantity,
                    "name": product.name,
                    "price": product.price,
                    "image_url": product.image_url
                })

    return jsonify({"cart": items}), 200

@cart.route('/delete_item/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_cart_item(item_id):
    customer_rut = get_jwt_identity()
    cart = Cart.query.filter_by(customer_rut=customer_rut).first()
    
    if not cart:
        return jsonify({"error": "Cart not found"}), 404

    cart_item = CartItem.query.filter_by(cart_id=cart.id, id=item_id).first()

    if not cart_item:
        return jsonify({"error": "Item not found in cart"}), 404

    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({"message": "Item deleted successfully"}), 200

@cart.route('/update_item/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    data = request.get_json()
    new_quantity = data.get("quantity")

    if not new_quantity or new_quantity < 1:
        return jsonify({"error": "Quantity must be greater than zero"}), 400

    customer_rut = get_jwt_identity()
    cart = Cart.query.filter_by(customer_rut=customer_rut).first()
    
    if not cart:
        return jsonify({"error": "Cart not found"}), 404

    cart_item = CartItem.query.filter_by(cart_id=cart.id, id=item_id).first()

    if not cart_item:
        return jsonify({"error": "Item not found in cart"}), 404

    cart_item.quantity = new_quantity
    db.session.commit()
    
    return jsonify({"message": "Item quantity updated successfully", "quantity": cart_item.quantity}), 200

@cart.route('/clear_items', methods=['DELETE'])
@jwt_required()
def clear_cart_items():
    customer_rut = get_jwt_identity()
    cart = Cart.query.filter_by(customer_rut=customer_rut).first()

    if not cart:
        return jsonify({"error": "Cart not found"}), 404

    CartItem.query.filter_by(cart_id=cart.id).delete()
    db.session.commit()
    return jsonify({"message": "All items cleared from cart"}), 200

@cart.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_cart():
    customer_rut = get_jwt_identity()
    cart = Cart.query.filter_by(customer_rut=customer_rut).first()

    if not cart:
        return jsonify({"error": "Cart not found"}), 404

    CartItem.query.filter_by(cart_id=cart.id).delete()
    db.session.delete(cart)
    db.session.commit()
    return jsonify({"message": "Cart and items deleted successfully"}), 200
