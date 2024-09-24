from .base import db
from sqlalchemy import Column, Integer, String, ForeignKey

class Usuario(db.Model):
    __tablename__ = 'usuario'
    rut = Column(String(12), primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=False)
    usuario = Column(String(50), unique=True, nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)

    rol_id = Column(Integer, ForeignKey('rol.id'), nullable=False)
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)

    def serializar(self):
        return {
            "rut": self.rut,
            "nombre": self.nombre,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "usuario": self.usuario,
            "correo": self.correo,
            "rol_id": self.rol_id,
            "cafeteria_id": self.cafeteria_id,
        }
