import cloudinary.uploader
from flask import Blueprint, request, jsonify
from extensions import db
from models.product import Product
from models.user import User
from werkzeug.security import check_password_hash

product = Blueprint("product", __name__, url_prefix="/product")

# Constante para item_type_id de productos unitarios
ITEM_TYPE_PRODUCT = 2

@product.route("/", methods=["GET"])
def get_products():
    """Obtiene todos los productos."""
    try:
        products = Product.query.all()
        return jsonify([product.serialize() for product in products]), 200
    except Exception as e:
        print(f"Error en /: {e}")
        return jsonify({"error": "Error al obtener productos", "details": str(e)}), 500

@product.route("/customer-request-products", methods=["GET"])
def get_customer_products():
    """Obtiene productos para clientes."""
    try:
        products = Product.query.all()
        return jsonify([product.serialize() for product in products]), 200
    except Exception as e:
        print(f"Error en /customer-request-products: {e}")
        return jsonify({"error": "Error al obtener productos", "details": str(e)}), 500

@product.route("/admin-get-products", methods=["GET"])
def get_admin_products():
    """Obtiene productos para el administrador."""
    try:
        print("Solicitud recibida en /admin-get-products")
        products = Product.query.all()
        print(f"Productos encontrados: {len(products)}")
        return jsonify([product.serialize() for product in products]), 200
    except Exception as e:
        print(f"Error en /admin-get-products: {e}")
        return jsonify({"error": "Error al obtener productos", "details": str(e)}), 500

@product.route("/create", methods=["POST"])
def create_product():
    """Crea un nuevo producto."""
    try:
        print("Solicitud para crear producto recibida")

        name = request.form.get("name")
        price = request.form.get("price")
        stock = request.form.get("stock")
        product_category_id = request.form.get("product_category_id")
        cafe_id = request.form.get("cafe_id")
        image_file = request.files.get("image")

        if not all([name, price, stock, product_category_id, cafe_id, image_file]):
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        upload_result = cloudinary.uploader.upload(
            image_file, folder="product", overwrite=True, resource_type="image"
        )
        print(f"Imagen subida a Cloudinary: {upload_result}")

        new_product = Product(
            name=name,
            price=float(price),
            stock=int(stock),
            product_category_id=int(product_category_id),
            cafe_id=int(cafe_id),
            image_url=upload_result["secure_url"],
            item_type_id=ITEM_TYPE_PRODUCT,
        )

        db.session.add(new_product)
        db.session.commit()

        print("Producto creado exitosamente")
        return jsonify({"message": "Producto creado exitosamente", "product": new_product.serialize()}), 201

    except Exception as e:
        print(f"Error al crear producto: {str(e)}")
        return jsonify({"error": str(e)}), 500

@product.route("/update/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """Actualiza un producto existente y elimina la imagen previa si es necesario."""
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Producto no encontrado"}), 404

        name = request.form.get("name")
        price = request.form.get("price")
        stock = request.form.get("stock")
        product_category_id = request.form.get("product_category_id")
        cafe_id = request.form.get("cafe_id")
        new_image = request.files.get("image")

        if name:
            product.name = name
        if price:
            product.price = float(price)
        if stock:
            product.stock = int(stock)
        if product_category_id:
            product.product_category_id = int(product_category_id)
        if cafe_id:
            product.cafe_id = int(cafe_id)

        if new_image:
            # Eliminar la imagen anterior si existe
            if product.image_url:
                try:
                    public_id = product.image_url.split("/")[-1].split(".")[0]
                    cloudinary.uploader.destroy(f"product/{public_id}")
                    print(f"Imagen previa eliminada: {public_id}")
                except Exception as e:
                    print(f"Error al eliminar imagen previa: {str(e)}")

            # Subir la nueva imagen
            upload_result = cloudinary.uploader.upload(
                new_image, folder="product", resource_type="image"
            )
            product.image_url = upload_result["secure_url"]

        db.session.commit()
        return jsonify({"message": "Producto actualizado exitosamente", "product": product.serialize()}), 200

    except Exception as e:
        print(f"Error al actualizar producto: {str(e)}")
        return jsonify({"error": str(e)}), 500

@product.route("/delete/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Elimina un producto."""
    try:
        print(f"Solicitud para eliminar producto con ID: {product_id}")
        data = request.get_json()
        print(f"Datos recibidos: {data}")

        admin_rut = data.get("admin_rut")
        admin_password = data.get("password")
        print(f"Admin RUT: {admin_rut}, Contraseña proporcionada: {admin_password}")

        if not admin_rut or not admin_password:
            print("Error: Faltan el RUT o la contraseña del administrador.")
            return jsonify({"error": "RUT y contraseña del administrador son requeridos"}), 400

        admin = User.query.filter_by(rut=admin_rut).first()
        if not admin:
            print(f"Error: No se encontró un administrador con el RUT {admin_rut}.")
            return jsonify({"error": "Administrador no encontrado"}), 404

        print(f"Hash almacenado en la base de datos: {admin.password}")
        try:
            # Validación con bcrypt como respaldo
            import bcrypt
            is_valid = bcrypt.checkpw(admin_password.encode('utf-8'), admin.password.encode('utf-8'))
            if not is_valid:
                print("Error: La contraseña proporcionada no coincide con el hash almacenado.")
                return jsonify({"error": "Contraseña incorrecta"}), 401
        except Exception as e:
            print(f"Error al verificar el hash de la contraseña: {e}")
            return jsonify({"error": "Hash de contraseña inválido en la base de datos.", "details": str(e)}), 500

        product = Product.query.get(product_id)
        if not product:
            print(f"Error: Producto con ID {product_id} no encontrado.")
            return jsonify({"error": "Producto no encontrado"}), 404

        if product.image_url:
            public_id = product.image_url.split("/")[-1].split(".")[0]
            cloudinary.uploader.destroy(f"product/{public_id}")

        db.session.delete(product)
        db.session.commit()
        print(f"Producto {product_id} eliminado exitosamente.")
        return jsonify({"message": "Producto eliminado exitosamente"}), 200

    except Exception as e:
        print(f"Error al eliminar producto: {str(e)}")
        return jsonify({"error": str(e)}), 500


@product.route("/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    """Obtiene los detalles de un producto por ID."""
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Producto no encontrado"}), 404

        return jsonify(product.serialize()), 200
    except Exception as e:
        print(f"Error al obtener producto por ID: {e}")
        return jsonify({"error": "Error al obtener producto", "details": str(e)}), 500