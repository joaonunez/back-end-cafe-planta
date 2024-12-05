from extensions import db

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Country(db.Model):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    states = relationship('State', backref='country', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
