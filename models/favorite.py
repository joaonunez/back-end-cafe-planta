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
    item_type = Column(String(50), nullable=False)  # Tipo de ítem ('product' o 'combo_menu')

    def serialize(self):
        return {
            "id": self.id,
            "customer_rut": self.customer_rut,
            "item_id": self.item_id,
            "item_type": self.item_type
        }

    # Método para asociar el ítem según su tipo
    def get_item(self):
        if self.item_type == 'product':
            return Product.query.get(self.item_id)
        elif self.item_type == 'combo_menu':
            return ComboMenu.query.get(self.item_id)
        else:
            return None
