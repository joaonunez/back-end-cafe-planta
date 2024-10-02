from .base import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class DiningArea(db.Model):
    __tablename__ = 'dining_area'
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, nullable=False)
    qr_code = Column(String(255), nullable=False)
    cafe_id = Column(Integer, ForeignKey('cafe.id'), nullable=False)

    cafe = relationship('Cafe')

    def serialize(self):
        return {
            "id": self.id,
            "number": self.number,
            "qr_code": self.qr_code,
            "cafe_id": self.cafe_id
        }
