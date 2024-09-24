from .base import db
from sqlalchemy import Column, Integer, String

class TipoItem(db.Model):
    __tablename__ = 'tipo_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        }
