from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from extensions import db, bcrypt
from models.dining_area import DiningArea
from models.user import User
import qrcode
import cloudinary.uploader
import io
import threading
from sqlalchemy.exc import IntegrityError

dining_area = Blueprint("dining_area", __name__, url_prefix="/dining_area")

qr_lock = threading.Lock()

@dining_area.route("/list", methods=["GET"])
def list_dining_areas():
    try:
        dining_areas = DiningArea.query.all()
        return jsonify([area.serialize() for area in dining_areas]), 200
    except Exception as e:
        print(f"Error al obtener las mesas: {str(e)}")
        return jsonify({"error": "Error al obtener las mesas"}), 500


@dining_area.route("/create", methods=["POST"])
def create_dining_area():
    try:
        data = request.get_json()
        number = data.get("number")
        cafe_id = data.get("cafe_id")

        if not number or not cafe_id:
            return jsonify({"error": "Número de mesa y ID del café son requeridos"}), 400

        new_dining_area = DiningArea(
            number=number,
            qr_code="",
            cafe_id=cafe_id
        )

        db.session.add(new_dining_area)
        db.session.commit()

        qr_data = json.dumps({"id": new_dining_area.id, "cafe_id": cafe_id})
        qr_image = qrcode.make(qr_data)
        buffered = io.BytesIO()
        qr_image.save(buffered, format="PNG")
        buffered.seek(0)

        public_id = f"qr_dining_area_{new_dining_area.id}_{cafe_id}"
        upload_result = cloudinary.uploader.upload(
            buffered,
            folder="qr_dining_area",
            public_id=public_id,
            resource_type="image"
        )

        new_dining_area.qr_code = upload_result["secure_url"]
        db.session.commit()

        return jsonify(new_dining_area.serialize()), 201

    except Exception as e:
        print(f"Error al crear la mesa: {str(e)}")
        return jsonify({"error": "Error al crear la mesa", "details": str(e)}), 500


@dining_area.route("/scan_qr", methods=["POST"])
def scan_qr():
    try:
        data = request.get_json()
        qr_content = data.get("qr_content")
        if not qr_content:
            return jsonify({"error": "El contenido del QR es requerido"}), 400

        if isinstance(qr_content, str):
            try:
                qr_data = json.loads(qr_content)
            except json.JSONDecodeError:
                return jsonify({"error": "El QR no contiene un JSON válido"}), 400
        elif isinstance(qr_content, dict):
            qr_data = qr_content
        else:
            return jsonify({"error": "El QR contiene un formato no válido"}), 400

        dining_area_id = qr_data.get("id")
        cafe_id = qr_data.get("cafe_id")

        if not dining_area_id or not cafe_id:
            return jsonify({"error": "El QR no contiene información válida"}), 400

        dining_area_obj = DiningArea.query.filter_by(id=dining_area_id, cafe_id=cafe_id).first()
        if not dining_area_obj:
            return jsonify({"error": "La mesa no existe"}), 404

        return jsonify(dining_area_obj.serialize()), 200

    except Exception as e:
        print(f"Error inesperado al procesar el QR: {str(e)}")
        return jsonify({"error": "Error interno al procesar el QR", "details": str(e)}), 500


@dining_area.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_dining_area(id):
    current_user_rut = get_jwt_identity()
    current_user = User.query.filter_by(rut=current_user_rut).first()

    if not current_user or current_user.role_id != 1:
        return jsonify({"error": "No está autorizado para eliminar mesas"}), 403

    data = request.get_json()
    admin_rut = data.get("admin_rut")
    admin_password = data.get("password")

    if current_user.rut != admin_rut:
        return jsonify({"error": "No coincide el rut del administrador"}), 401

    if not bcrypt.check_password_hash(current_user.password, admin_password):
        return jsonify({"error": "Contraseña de administrador incorrecta"}), 401

    dining_area_to_delete = DiningArea.query.get(id)
    if not dining_area_to_delete:
        return jsonify({"error": "Mesa no encontrada"}), 404

    # Primero intentamos eliminar el registro de la base de datos
    try:
        db.session.delete(dining_area_to_delete)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        # No eliminar de Cloudinary si no se pudo eliminar en DB
        return jsonify({"error": "No se puede eliminar la mesa porque tiene ventas registradas asociadas."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar la mesa: {str(e)}"}), 500

    # Si la eliminación en la base de datos fue exitosa, entonces eliminar el QR de Cloudinary
    cloudinary_public_id = f"qr_dining_area/qr_dining_area_{dining_area_to_delete.id}_{dining_area_to_delete.cafe_id}"
    try:
        cloudinary.uploader.destroy(cloudinary_public_id)
    except Exception as e:
        print(f"Error al eliminar imagen de Cloudinary: {e}")

    return jsonify({"message": "Mesa eliminada exitosamente"}), 200
