from extensions import db

from sqlalchemy import Column, Integer, String

class Customer(db.Model):
    __tablename__ = 'customer'
    rut = Column(String(12), primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    username = Column(String(50), unique=True, nullable=False)

    def serialize(self):
        return {
            "rut": self.rut,
            "name": self.name,
            "email": self.email,
            "username": self.username,
        }
