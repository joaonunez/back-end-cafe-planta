from .base import db
from sqlalchemy import Column, Integer, ForeignKey

class CartItem(db.Model):
    __tablename__ = 'cart_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey('cart.id'), nullable=False)  # Relación con el carrito
    item_id = Column(Integer, nullable=False)  # ID del producto o combo
    item_type_id = Column(Integer, ForeignKey('item_type.id'), nullable=False)  # Tipo de ítem (producto o combo)
    quantity = Column(Integer, nullable=False, default=1)  # Cantidad de ítems agregados

    cart = relationship('Cart', backref='items')  # Relación con el carrito

    def serialize(self):
        return {
            "id": self.id,
            "cart_id": self.cart_id,
            "item_id": self.item_id,
            "item_type_id": self.item_type_id,
            "quantity": self.quantity,
        }
