from flask import Blueprint, jsonify
import cloudinary.api

cloudinary_bp = Blueprint("cloudinary", __name__, url_prefix="/cloudinary")

@cloudinary_bp.route("/stats", methods=["GET"])
def get_cloudinary_stats():
    """
    Endpoint para obtener estadísticas de Cloudinary.
    Devuelve información sobre el espacio usado y disponible.
    """
    try:
        print("Solicitando estadísticas de Cloudinary...")
        stats = cloudinary.api.usage()
        print(f"Estadísticas recibidas: {stats}")
        
        # Usar "usage" en la sección de storage para el espacio usado
        used_space = stats.get("storage", {}).get("usage", 0) / (1024**3)  # Convertir bytes a GB
        
        # Establecemos el límite del plan (25 GB para el plan gratuito)
        total_space = 25  # Límite de almacenamiento del plan gratuito en GB
        
        percentage_used = (used_space / total_space) * 100

        return jsonify({
            "used_space": used_space,
            "total_space": total_space,
            "percentage_used": percentage_used,
            "status": "success"
        }), 200
    except cloudinary.exceptions.Error as e:
        print(f"Error de Cloudinary: {e}")
        return jsonify({"error": f"Cloudinary API Error: {str(e)}"}), 500
    except Exception as e:
        print(f"Error general: {e}")
        return jsonify({"error": f"Error general: {str(e)}"}), 500


