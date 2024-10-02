from .base import db
from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from datetime import datetime

class ProductRating(db.Model):
    __tablename__ = 'product_rating'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_rut = Column(String(12), ForeignKey('customer.rut'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    rating = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)

    def serialize(self):
        return {
            "id": self.id,
            "customer_rut": self.customer_rut,
            "product_id": self.product_id,
            "rating": self.rating,
            "date": self.date,
        }
