from .base import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Pais(db.Model):
    __tablename__ = 'pais'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    regiones = relationship('Region', backref='pais', lazy=True)

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        }
