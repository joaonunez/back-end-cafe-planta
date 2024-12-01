import cloudinary.uploader
from flask import Blueprint, request, jsonify
from extensions import db
from models.product import Product

product = Blueprint("product", __name__, url_prefix="/product")

# Establecer un valor fijo para item_type_id
ITEM_TYPE_PRODUCT = 2  # ID correspondiente al tipo "Producto Unitario"

@product.route("/", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])

@product.route("/customer-request-products", methods=["GET"])
def get_customer_products():
    products = Product.query.all()
    return jsonify([product.serialize() for product in products]), 200

@product.route("/admin-get-products", methods=["GET"])
def get_admin_products():
    products = Product.query.all()
    return jsonify([product.serialize() for product in products]), 200

@product.route("/create", methods=["POST"])
def create_product():
    try:
        print("Solicitud para crear producto recibida")

        # Obtener datos del formulario
        name = request.form.get("name")
        price = request.form.get("price")
        stock = request.form.get("stock")
        product_category_id = request.form.get("product_category_id")
        cafe_id = request.form.get("cafe_id")
        image_file = request.files.get("image")

        print(f"Datos recibidos - Name: {name}, Price: {price}, Stock: {stock}, Category: {product_category_id}, Cafe: {cafe_id}, Image: {image_file}")

        if not all([name, price, stock, product_category_id, cafe_id, image_file]):
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        # Subir la imagen a Cloudinary en el folder `/product`
        print("Subiendo imagen a Cloudinary...")
        upload_result = cloudinary.uploader.upload(
            image_file,
            folder="product",  # Guardar en el directorio `/product`
            overwrite=True,     # Reemplazar si ya existe con el mismo nombre
            resource_type="image"  # Tipo de recurso: imagen
        )
        print(f"Imagen subida a Cloudinary: {upload_result}")

        # Crear un nuevo producto en la base de datos
        print("Creando producto en la base de datos...")
        new_product = Product(
            name=name,
            price=float(price),
            stock=int(stock),
            product_category_id=int(product_category_id),
            cafe_id=int(cafe_id),
            image_url=upload_result["secure_url"],  # URL segura de Cloudinary
            item_type_id=ITEM_TYPE_PRODUCT  # Valor fijo para productos
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
    try:
        # Obtener producto existente
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Producto no encontrado"}), 404

        # Obtener datos del formulario
        name = request.form.get("name")
        price = request.form.get("price")
        stock = request.form.get("stock")
        product_category_id = request.form.get("product_category_id")
        cafe_id = request.form.get("cafe_id")
        new_image = request.files.get("image")

        # Actualizar los campos proporcionados
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

        # Si hay una nueva imagen, eliminar la antigua de Cloudinary y subir la nueva
        if new_image:
            if product.image_url:
                public_id = product.image_url.split("/")[-1].split(".")[0]  # Obtener public_id de la URL
                cloudinary.uploader.destroy(f"product/{public_id}")  # Eliminar la imagen antigua

            # Subir la nueva imagen
            upload_result = cloudinary.uploader.upload(
                new_image,
                folder="product",
                resource_type="image"
            )
            product.image_url = upload_result["secure_url"]

        db.session.commit()

        return jsonify({"message": "Producto actualizado exitosamente", "product": product.serialize()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500