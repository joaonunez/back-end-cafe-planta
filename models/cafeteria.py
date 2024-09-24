from .base import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Cafeteria(db.Model):
    __tablename__ = 'cafeteria'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=False)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)

    comuna = relationship('Comuna', backref='cafeterias')

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "comuna_id": self.comuna_id,
        }
