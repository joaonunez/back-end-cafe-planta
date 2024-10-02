from .base import db
from sqlalchemy import Column, Integer, String

class ItemType(db.Model):
    __tablename__ = 'item_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
