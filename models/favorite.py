from extensions import db
from .combo_menu import ComboMenu
from .product import Product
from sqlalchemy import Column, Integer, String, ForeignKey

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_rut = Column(String(12), ForeignKey('customer.rut'), nullable=False)

    # Polimorfismo: el item puede ser un Product o un ComboMenu
    item_id = Column(Integer, nullable=False)  # ID del ítem (producto o combo)
    item_type_id = Column(Integer, ForeignKey('item_type.id'), nullable=False)  # Referencia a ItemType

    # Relación con ItemType
    item_type = db.relationship('ItemType')

    def serialize(self):
        item = self.get_item()  # Obtenemos el objeto producto o combo usando el método get_item
        return {
            "id": self.id,
            "item_id": self.item_id,
            "item_name": item.name if item else None,  # Nombre del producto o combo
            "item_type_id": self.item_type_id,  # Tipo de ítem (1 = Combo, 2 = Producto)
            "price": item.price if item else None,  # Precio del producto o combo
            "image_url": item.image_url if item else None,  # URL de la imagen
            "cafe_id": getattr(item, 'cafe_id', None),  # ID de la cafetería asociada
            "cafe_name": getattr(item, 'cafe_name', None),  # Nombre de la cafetería (si está disponible)
            "stock": getattr(item, 'stock', None),  # Solo los productos tienen stock
            "description": getattr(item, 'description', None)  # Solo combos podrían tener descripción
        }

    def get_item(self):
        """
        Devuelve la instancia del Producto o Combo correspondiente al `item_type_id`.
        """
        if self.item_type_id == 2:  # Producto
            return Product.query.get(self.item_id)
        elif self.item_type_id == 1:  # Combo
            return ComboMenu.query.get(self.item_id)
        return None
