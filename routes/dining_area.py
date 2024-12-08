from flask import Blueprint, jsonify, request
import json
from extensions import db
from models.dining_area import DiningArea
import qrcode
import cloudinary.uploader
import io
import threading

dining_area = Blueprint("dining_area", __name__, url_prefix="/dining_area")

# Lock para evitar solicitudes simultáneas en el endpoint /scan_qr
qr_lock = threading.Lock()

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

        # Crear el objeto de mesa sin adulterar el ID autoincremental
        new_dining_area = DiningArea(
            number=number,
            qr_code="",  # Se genera después del commit para obtener el ID autoincrementado
            cafe_id=cafe_id
        )

        db.session.add(new_dining_area)
        db.session.commit()

        # Crear contenido del QR con el ID ya generado
        qr_data = json.dumps({"id": new_dining_area.id, "cafe_id": cafe_id})
        qr_image = qrcode.make(qr_data)

        # Guardar el QR en memoria
        buffered = io.BytesIO()
        qr_image.save(buffered, format="PNG")
        buffered.seek(0)

        # Subir el QR a Cloudinary
        upload_result = cloudinary.uploader.upload(
            buffered,
            folder="qr_dining_area",
            public_id=f"qr_dining_area_{new_dining_area.id}_{cafe_id}",
            resource_type="image"
        )

        # Actualizar el QR code en el registro de la base de datos
        new_dining_area.qr_code = upload_result["secure_url"]
        db.session.commit()

        return jsonify(new_dining_area.serialize()), 201

    except Exception as e:
        print(f"Error al crear la mesa: {str(e)}")
        return jsonify({"error": "Error al crear la mesa", "details": str(e)}), 500


@dining_area.route("/scan_qr", methods=["POST"])
def scan_qr():
    """Procesa el contenido de un QR y devuelve información de la mesa."""
    try:
        print("Inicio del endpoint /scan_qr")
        data = request.get_json()
        print(f"Datos recibidos en la solicitud: {data}")
        
        qr_content = data.get("qr_content")
        if not qr_content:
            return jsonify({"error": "El contenido del QR es requerido"}), 400

        # Si qr_content es un string, decodificarlo
        if isinstance(qr_content, str):
            try:
                qr_data = json.loads(qr_content)
            except json.JSONDecodeError:
                return jsonify({"error": "El QR no contiene un JSON válido"}), 400
        elif isinstance(qr_content, dict):
            qr_data = qr_content  # Ya es un diccionario
        else:
            return jsonify({"error": "El QR contiene un formato no válido"}), 400

        dining_area_id = qr_data.get("id")
        cafe_id = qr_data.get("cafe_id")

        if not dining_area_id or not cafe_id:
            return jsonify({"error": "El QR no contiene información válida"}), 400

        # Buscar la mesa en la base de datos
        dining_area = DiningArea.query.filter_by(id=dining_area_id, cafe_id=cafe_id).first()
        if not dining_area:
            return jsonify({"error": "La mesa no existe"}), 404

        print(f"Mesa encontrada: {dining_area.serialize()}")
        return jsonify(dining_area.serialize()), 200

    except Exception as e:
        print(f"Error inesperado al procesar el QR: {str(e)}")
        return jsonify({"error": "Error interno al procesar el QR", "details": str(e)}), 500
