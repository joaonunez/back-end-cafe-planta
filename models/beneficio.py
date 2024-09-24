from .base import db
from sqlalchemy import Column, Integer, String

class Beneficio(db.Model):
    __tablename__ = 'beneficio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    precio = Column(Integer, nullable=False)
    descripcion = Column(String(255), nullable=False)

    def serializar(self):
        return {
            "id": self.id,
            "precio": self.precio,
            "descripcion": self.descripcion,
        }
