from .base import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

class Venta(db.Model):
    __tablename__ = 'venta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, nullable=False, default=datetime.now)
    monto_total = Column(Integer, nullable=False)
    estado = Column(String(50), nullable=False, default="pendiente")
    comentarios = Column(Text, nullable=True)

    cliente_rut = Column(String(12), ForeignKey('cliente.rut'), nullable=False)
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    mesero_rut = Column(String(12), ForeignKey('usuario.rut'), nullable=True)
    mesa_id = Column(Integer, ForeignKey('mesa.id'), nullable=True)

    cliente = relationship('Cliente')
    cafeteria = relationship('Cafeteria')
    mesero = relationship('Usuario')
    mesa = relationship('Mesa')

    def serializar(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "monto_total": self.monto_total,
            "estado": self.estado,
            "comentarios": self.comentarios,
            "cliente_rut": self.cliente_rut,
            "cafeteria_id": self.cafeteria_id,
            "mesero_rut": self.mesero_rut,
            "mesa_id": self.mesa_id,
        }
