from .base import db
from sqlalchemy import Column, Integer, String, ForeignKey

class Comuna(db.Model):
    __tablename__ = 'comuna'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "region_id": self.region_id,
        }
