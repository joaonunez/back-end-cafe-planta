from .base import db
from sqlalchemy import Column, Integer, String, ForeignKey

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_rut = Column(String(12), ForeignKey('customer.rut'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "customer_rut": self.customer_rut,
            "product_id": self.product_id,
        }
