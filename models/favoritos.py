from .base import db
from sqlalchemy import Column, Integer, String, ForeignKey

class Favoritos(db.Model):
    __tablename__ = 'favoritos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_rut = Column(String(12), ForeignKey('cliente.rut'), nullable=False)
    producto_id = Column(Integer, ForeignKey('producto.id'), nullable=False)

    def serializar(self):
        return {
            "id": self.id,
            "cliente_rut": self.cliente_rut,
            "producto_id": self.producto_id,
        }
