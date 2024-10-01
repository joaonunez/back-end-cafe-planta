from .base import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Cafe(db.Model):
    __tablename__ = 'cafe'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)

    city = relationship('City', backref='cafes')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "city_id": self.city_id,
        }
