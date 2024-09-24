from .base import db
from sqlalchemy import Column, Integer, ForeignKey

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    venta_id = Column(Integer, ForeignKey('venta.id'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Integer, nullable=False)
    tipo_item_id = Column(Integer, ForeignKey('tipo_item.id'), nullable=False)
    item_id = Column(Integer, nullable=False)

    def serializar(self):
        return {
            "id": self.id,
            "venta_id": self.venta_id,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "tipo_item_id": self.tipo_item_id,
            "item_id": self.item_id,
        }
