from flask import Blueprint, request, jsonify
from models import Favorite, Product, ComboMenu
from extensions import db
from models.favorite import Favorite
from flask_jwt_extended import jwt_required, get_jwt_identity
favorite = Blueprint("favorite", __name__, url_prefix="/favorite")


# Endpoint para agregar un favorito
@favorite.route("/add-to-favorites-customer", methods=["POST"])
@jwt_required()
def add_favorite():
    data = request.get_json()
    customer_rut = get_jwt_identity()
    item_id = data.get("item_id")
    item_type_id = data.get("item_type_id")  # Cambiado a int

    if not item_id or not item_type_id:
        return jsonify({"error": "Item ID and type are required"}), 400

    # Crear un nuevo favorito
    new_favorite = Favorite(customer_rut=customer_rut, item_id=item_id, item_type_id=item_type_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()), 201

@favorite.route("/list-favorites-customer", methods=["GET"])
@jwt_required()
def list_favorites():
    try:
        customer_rut = get_jwt_identity()

        # Obtener todos los favoritos del cliente
        favorites = Favorite.query.filter_by(customer_rut=customer_rut).all()

        if not favorites:
            return jsonify([]), 200

        favorite_items = []
        for favorite in favorites:
            item = favorite.get_item()  # Obtener el producto o combo
            if item:
                favorite_items.append({
                    "favorite_id": favorite.id,  # ID del favorito en la tabla de favoritos
                    "item_id": favorite.item_id,  # ID del producto o combo
                    "item_type_id": favorite.item_type_id,  # Tipo de ítem (1 = Combo, 2 = Producto)
                    "item_name": item.name,  # Nombre del producto o combo
                    "price": getattr(item, 'price', None),  # Precio del producto o combo
                    "image_url": getattr(item, 'image_url', None),  # URL de la imagen
                    "cafe_id": getattr(item, 'cafe_id', None),  # ID de la cafetería asociada
                    "cafe_name": getattr(item, 'cafe_name', None),  # Nombre de la cafetería
                    "stock": getattr(item, 'stock', None),  # Solo los productos tienen stock
                    "description": getattr(item, 'description', None)  # Solo los combos tienen descripción
                })
            else:
                print(f"Elemento no encontrado para favorito con id: {favorite.id}")

        # Retornar los favoritos encontrados en formato JSON
        return jsonify(favorite_items), 200
    except Exception as e:
        print(f"Error listando favoritos: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500





# Endpoint para eliminar un favorito
@favorite.route("/remove-favorite-customer", methods=["DELETE"])
@jwt_required()
def remove_favorite():
    data = request.get_json()
    customer_rut = get_jwt_identity()  # Obtener la identidad del cliente autenticado
    item_id = data.get("item_id")
    item_type_id = data.get("item_type_id")  # Cambiado a int

    if not item_id or not item_type_id:
        return jsonify({"error": "Item ID and type are required"}), 400

    # Buscar el favorito que se quiere eliminar
    favorite = Favorite.query.filter_by(customer_rut=customer_rut, item_id=item_id, item_type_id=item_type_id).first()

    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    # Eliminar el favorito de la base de datos
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite removed successfully"}), 200