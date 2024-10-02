from .base import db
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
            "item_name": item.name if item else None,  # Aquí accedemos al nombre del producto o combo
            "item_type_id": self.item_type_id  # Aseguramos que el front-end sepa si es producto o combo
        }


    def get_item(self):
        if self.item_type_id == 2:  # Si es un producto
            return Product.query.get(self.item_id)
        elif self.item_type_id == 1:  # Si es un combo
            return ComboMenu.query.get(self.item_id)
        return None


