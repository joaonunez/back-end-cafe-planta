from .base import db
from sqlalchemy import Column, Integer, String, ForeignKey

class City(db.Model):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    state_id = Column(Integer, ForeignKey('state.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "state_id": self.state_id,
        }
