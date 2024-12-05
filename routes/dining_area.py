from flask import Blueprint, jsonify, request, json
from extensions import db
from models.dining_area import DiningArea
import qrcode
import cloudinary.uploader
import io

dining_area = Blueprint("dining_area", __name__, url_prefix="/dining_area")

@dining_area.route("/list", methods=["GET"])
def list_dining_areas():
    """Obtiene todas las mesas disponibles."""
    try:
        dining_areas = DiningArea.query.all()
        return jsonify([area.serialize() for area in dining_areas]), 200
    except Exception as e:
        print(f"Error al obtener las mesas: {str(e)}")
        return jsonify({"error": "Error al obtener las mesas"}), 500


@dining_area.route("/create", methods=["POST"])
def create_dining_area():
    """Crea una nueva mesa con QR generado."""
    try:
        data = request.get_json()
        number = data.get("number")
        cafe_id = data.get("cafe_id")

        if not number or not cafe_id:
            return jsonify({"error": "Número de mesa y ID del café son requeridos"}), 400

        # Crear contenido del QR en formato JSON
        qr_data = json.dumps({"id": number, "number": number, "cafe_id": cafe_id})
        qr_image = qrcode.make(qr_data)

        # Guardar el QR en memoria
        buffered = io.BytesIO()
        qr_image.save(buffered, format="PNG")
        buffered.seek(0)

        # Subir el QR a Cloudinary
        upload_result = cloudinary.uploader.upload(
            buffered,
            folder="qr_dining_area",
            public_id=f"qr_dining_area_{number}_{cafe_id}",
            resource_type="image"
        )

        # Crear el objeto de mesa
        new_dining_area = DiningArea(
            number=number,
            qr_code=upload_result["secure_url"],
            cafe_id=cafe_id
        )

        db.session.add(new_dining_area)
        db.session.commit()

        return jsonify(new_dining_area.serialize()), 201

    except Exception as e:
        print(f"Error al crear la mesa: {str(e)}")
        return jsonify({"error": "Error al crear la mesa", "details": str(e)}), 500


