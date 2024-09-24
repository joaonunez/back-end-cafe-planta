from .base import db
from sqlalchemy import Column, Integer, String

class Rol(db.Model):
    __tablename__ = 'rol'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    salario_base = Column(Integer, nullable=False)

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "salario_base": self.salario_base,
        }
