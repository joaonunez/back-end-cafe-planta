from .base import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Mesa(db.Model):
    __tablename__ = 'mesa'
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer, nullable=False)
    qr_code = Column(String(255), nullable=False)
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)

    cafeteria = relationship('Cafeteria')

    def serializar(self):
        return {
            "id": self.id,
            "numero": self.numero,
            "qr_code": self.qr_code,
            "cafeteria_id": self.cafeteria_id
        }
