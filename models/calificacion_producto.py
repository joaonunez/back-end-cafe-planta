from .base import db
from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from datetime import datetime

class CalificacionProducto(db.Model):
    __tablename__ = 'calificacion_producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_rut = Column(String(12), ForeignKey('cliente.rut'), nullable=False)
    producto_id = Column(Integer, ForeignKey('producto.id'), nullable=False)
    calificacion = Column(Float, nullable=False)
    fecha = Column(DateTime, nullable=False, default=datetime.now)

    def serializar(self):
        return {
            "id": self.id,
            "cliente_rut": self.cliente_rut,
            "producto_id": self.producto_id,
            "calificacion": self.calificacion,
            "fecha": self.fecha,
        }
