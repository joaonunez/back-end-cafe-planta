from extensions import db

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Cart(db.Model):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_rut = Column(String(12), ForeignKey('customer.rut'), nullable=False)  # Relación con el cliente
    created_at = Column(DateTime, default=datetime.now, nullable=False)  # Fecha de creación del carrito
    updated_at = Column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now)  # Última actualización

    customer = relationship('Customer', backref='carts')  # Relación con el cliente

    def serialize(self):
        return {
            "id": self.id,
            "customer_rut": self.customer_rut,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
