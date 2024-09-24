from .base import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Region(db.Model):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    pais_id = Column(Integer, ForeignKey('pais.id'), nullable=False)
    comunas = relationship('Comuna', backref='region', lazy=True)

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "pais_id": self.pais_id,
        }
