import cloudinary.uploader
from flask import Blueprint, request, jsonify
import json
from extensions import db
from models.combo_menu import ComboMenu
from models.product import Product
from models.user import User

combo_menu = Blueprint("combo_menu", __name__, url_prefix="/combo_menu")

@combo_menu.route("/", methods=["GET"])
def get_combo_menus():
    """
    Obtiene todos los combos disponibles.
    """
    try:
        combos = ComboMenu.query.all()
        return jsonify([combo.serialize() for combo in combos]), 200
    except Exception as e:
        print(f"Error al obtener combos: {e}")
        return jsonify({"error": "Error al obtener combos", "details": str(e)}), 500


@combo_menu.route('/bulk', methods=['POST'])
def create_combos_bulk():
    """
    Crea múltiples combos de forma masiva.
    """
    try:
        data = request.get_json()

        if not isinstance(data, list):
            return jsonify({"error": "Expected a list of combos"}), 400

        new_combos = []
        for combo_data in data:
            name = combo_data.get('name')
            price = combo_data.get('price')
            cafe_id = combo_data.get('cafe_id')
            item_type_id = combo_data.get('item_type_id')

            if not all([name, price, cafe_id, item_type_id]):
                return jsonify({"error": "Missing required fields"}), 400

            new_combo = ComboMenu(
                name=name,
                price=price,
                cafe_id=cafe_id,
                item_type_id=item_type_id
            )
            db.session.add(new_combo)
            new_combos.append(new_combo)

        db.session.commit()
        return jsonify([combo.serialize() for combo in new_combos]), 201
    except Exception as e:
        print(f"Error al crear combos masivamente: {e}")
        return jsonify({"error": "Error al crear combos", "details": str(e)}), 500


@combo_menu.route("/customer-request-combos", methods=["GET"])
def get_customer_combos():
    """
    Obtiene todos los combos disponibles para los clientes.
    """
    try:
        combos = ComboMenu.query.all()
        return jsonify([combo.serialize() for combo in combos]), 200
    except Exception as e:
        print(f"Error al obtener combos para clientes: {e}")
        return jsonify({"error": "Error al obtener combos", "details": str(e)}), 500


@combo_menu.route("/admin-get-combos", methods=["GET"])
def get_admin_combos():
    """
    Obtiene todos los combos disponibles para el administrador.
    Incluye los productos asociados a cada combo.
    """
    try:
        combos = ComboMenu.query.all()
        if not combos:
            return jsonify({"message": "No hay combos disponibles"}), 200

        return jsonify([combo.serialize() for combo in combos]), 200
    except Exception as e:
        print(f"Error al obtener combos para el administrador: {e}")
        return jsonify({"error": "Error al obtener combos", "details": str(e)}), 500


@combo_menu.route("/search-products", methods=["GET"])
def search_products():
    """
    Busca productos según el término ingresado.
    """
    try:
        term = request.args.get("term", "").lower()
        if not term:
            return jsonify({"error": "El término de búsqueda es obligatorio"}), 400

        products = Product.query.filter(Product.name.ilike(f"%{term}%")).all()
        return jsonify([product.serialize() for product in products]), 200
    except Exception as e:
        print(f"Error al buscar productos: {e}")
        return jsonify({"error": "Error al buscar productos", "details": str(e)}), 500


@combo_menu.route("/get-combo/<int:combo_id>", methods=["GET"])
def get_combo(combo_id):
    """
    Obtiene los detalles de un combo específico por su ID.
    """
    try:
        combo = ComboMenu.query.get(combo_id)
        if not combo:
            return jsonify({"error": "Combo no encontrado"}), 404

        return jsonify(combo.serialize()), 200
    except Exception as e:
        print(f"Error al obtener el combo: {e}")
        return jsonify({"error": "Error al obtener el combo", "details": str(e)}), 500


@combo_menu.route("/update-combo/<int:combo_id>", methods=["PUT"])
def update_combo(combo_id):
    """
    Actualiza un combo existente y maneja los productos asociados e imagen.
    """
    try:
        combo = ComboMenu.query.get(combo_id)
        if not combo:
            return jsonify({"error": "Combo no encontrado"}), 404

        # Obtener datos del formulario
        name = request.form.get("name")
        price = request.form.get("price")
        cafe_id = request.form.get("cafe_id")
        products = request.form.get("products")  # Vendrá como un JSON string
        new_image = request.files.get("image")

        # Logs para depuración
        print("Datos recibidos en el formulario:")
        print("Nombre:", name)
        print("Precio:", price)
        print("Sede ID:", cafe_id)
        print("Productos:", products)
        print("Archivo de imagen:", new_image)

        # Procesar productos
        if products:
            try:
                product_ids = json.loads(products)  # Convertir JSON string a lista
                print("Productos procesados:", product_ids)
                product_objects = Product.query.filter(Product.id.in_(product_ids)).all()
                combo.products = product_objects  # Actualizar relación
            except Exception as e:
                print("Error al procesar productos:", e)
                return jsonify({"error": "Formato inválido para los productos", "details": str(e)}), 400

        # Actualizar los campos del combo
        if name:
            combo.name = name
        if price:
            combo.price = float(price)
        if cafe_id:
            combo.cafe_id = int(cafe_id)

        # Manejar nueva imagen
        if new_image:
            # Eliminar imagen previa si existe
            if combo.image_url:
                try:
                    public_id = combo.image_url.split("/")[-1].split(".")[0]
                    cloudinary.uploader.destroy(f"combos/{public_id}")
                    print(f"Imagen previa eliminada: {public_id}")
                except Exception as e:
                    print(f"Error al eliminar imagen previa: {e}")

            # Subir la nueva imagen
            upload_result = cloudinary.uploader.upload(
                new_image, folder="combos", resource_type="image"
            )
            combo.image_url = upload_result["secure_url"]
            print(f"Nueva imagen subida: {combo.image_url}")

        # Guardar cambios en la base de datos
        db.session.commit()
        print("Combo actualizado exitosamente:", combo.serialize())
        return jsonify({"message": "Combo actualizado exitosamente", "combo": combo.serialize()}), 200

    except Exception as e:
        print(f"Error al actualizar combo: {e}")
        return jsonify({"error": "Error al actualizar combo", "details": str(e)}), 500


@combo_menu.route("/create", methods=["POST"])
def create_combo():
    """
    Crea un nuevo combo, incluyendo productos asociados e imagen.
    """
    try:
        # Obtener datos del formulario
        name = request.form.get("name")
        price = request.form.get("price")
        cafe_id = request.form.get("cafe_id")
        products = request.form.get("products")  # Lista en formato JSON
        image = request.files.get("image")

        # Validaciones
        if not all([name, price, cafe_id]):
            return jsonify({"error": "Nombre, precio y sede son obligatorios"}), 400

        # Subir imagen si existe
        image_url = None
        if image:
            upload_result = cloudinary.uploader.upload(
                image, folder="combos", resource_type="image"
            )
            image_url = upload_result["secure_url"]

        # Crear el combo
        new_combo = ComboMenu(
            name=name,
            price=int(price),
            cafe_id=int(cafe_id),
            image_url=image_url,
            item_type_id=1  # ID para el tipo de item Combo
        )

        # Asociar productos al combo
        if products:
            try:
                product_ids = json.loads(products)  # Convertir JSON string a lista
                product_objects = Product.query.filter(Product.id.in_(product_ids)).all()
                new_combo.products.extend(product_objects)
            except Exception as e:
                return jsonify({"error": "Formato inválido en productos", "details": str(e)}), 400

        db.session.add(new_combo)
        db.session.commit()

        return jsonify({"message": "Combo creado exitosamente", "combo": new_combo.serialize()}), 201

    except Exception as e:
        print(f"Error al crear combo: {e}")
        return jsonify({"error": "Error al crear combo", "details": str(e)}), 500

@combo_menu.route("/delete/<int:combo_id>", methods=["DELETE"])
def delete_combo(combo_id):
    """Elimina un combo, incluyendo su imagen en Cloudinary."""
    try:
        print(f"Solicitud para eliminar combo con ID: {combo_id}")
        data = request.get_json()
        print(f"Datos recibidos: {data}")

        admin_rut = data.get("admin_rut")
        admin_password = data.get("password")
        print(f"Admin RUT: {admin_rut}, Contraseña proporcionada: {admin_password}")

        # Validar RUT y contraseña del administrador
        if not admin_rut or not admin_password:
            print("Error: Faltan el RUT o la contraseña del administrador.")
            return jsonify({"error": "RUT y contraseña del administrador son requeridos"}), 400

        admin = User.query.filter_by(rut=admin_rut).first()
        if not admin:
            print(f"Error: No se encontró un administrador con el RUT {admin_rut}.")
            return jsonify({"error": "Administrador no encontrado"}), 404

        print(f"Hash almacenado en la base de datos: {admin.password}")
        try:
            # Validación con bcrypt
            import bcrypt
            is_valid = bcrypt.checkpw(admin_password.encode('utf-8'), admin.password.encode('utf-8'))
            if not is_valid:
                print("Error: La contraseña proporcionada no coincide con el hash almacenado.")
                return jsonify({"error": "Contraseña incorrecta"}), 401
        except Exception as e:
            print(f"Error al verificar el hash de la contraseña: {e}")
            return jsonify({"error": "Hash de contraseña inválido en la base de datos.", "details": str(e)}), 500

        # Buscar combo
        combo = ComboMenu.query.get(combo_id)
        if not combo:
            print(f"Error: Combo con ID {combo_id} no encontrado.")
            return jsonify({"error": "Combo no encontrado"}), 404

        # Eliminar imagen en Cloudinary si existe
        if combo.image_url:
            try:
                parsed_url = combo.image_url.split("/")
                folder_and_name = "/".join(parsed_url[-2:])  # Carpeta y nombre del archivo
                public_id = folder_and_name.split(".")[0]  # Sin extensión
                cloudinary.uploader.destroy(public_id)  # Usa el public_id completo
                print(f"Imagen eliminada correctamente: {public_id}")
            except Exception as e:
                print(f"Error al eliminar la imagen en Cloudinary: {str(e)}")

        # Eliminar el combo de la base de datos
        db.session.delete(combo)
        db.session.commit()
        print(f"Combo {combo_id} eliminado exitosamente.")
        return jsonify({"message": "Combo eliminado exitosamente"}), 200

    except Exception as e:
        print(f"Error al eliminar combo: {str(e)}")
        return jsonify({"error": "Error al eliminar combo", "details": str(e)}), 500