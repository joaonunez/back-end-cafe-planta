from .base import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .detalle_combo_menu import detalle_combo_menu  # Importar la tabla intermedia

class Producto(db.Model):
    __tablename__ = 'producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    
    categoria_producto_id = Column(Integer, ForeignKey('categoria_producto.id'), nullable=False)
    categoria_producto = relationship('CategoriaProducto', backref='productos')
    
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    cafeteria = relationship('Cafeteria', backref='productos')
    
    tipo_item_id = Column(Integer, ForeignKey('tipo_item.id'), nullable=False)
    tipo_item = relationship('TipoItem')

    # Cambiar el nombre del backref para evitar conflictos
    combos = relationship('ComboMenu', secondary=detalle_combo_menu, backref='productos_en_combo')

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
            "categoria_producto_id": self.categoria_producto_id,
            "cafeteria_id": self.cafeteria_id,
            "tipo_item_id": self.tipo_item_id,
        }
