from .base import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .detalle_combo_menu import detalle_combo_menu  # Importar la tabla intermedia

class ComboMenu(db.Model):
    __tablename__ = 'combo_menu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Integer, nullable=False)
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    tipo_item_id = Column(Integer, ForeignKey('tipo_item.id'), nullable=False)

    cafeteria = relationship('Cafeteria')
    tipo_item = relationship('TipoItem')

    # Cambiar el nombre del backref para evitar conflictos
    productos = relationship('Producto', secondary=detalle_combo_menu, backref='combo_menus')

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "cafeteria_id": self.cafeteria_id,
            "tipo_item_id": self.tipo_item_id,
            "productos": [producto.serializar() for producto in self.productos]
        }
