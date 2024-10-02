from .base import db
from sqlalchemy import Column, Integer, String

class Benefit(db.Model):
    __tablename__ = 'benefit'
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "price": self.price,
            "description": self.description,
        }
