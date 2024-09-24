from .base import db
from sqlalchemy import Column, Integer, String

class Cliente(db.Model):
    __tablename__ = 'cliente'
    rut = Column(String(12), primary_key=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    usuario = Column(String(50), unique=True, nullable=False)

    def serializar(self):
        return {
            "rut": self.rut,
            "nombre": self.nombre,
            "correo": self.correo,
            "usuario": self.usuario,
        }
