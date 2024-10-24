from extensions import db

from sqlalchemy import Column, Integer, String, ForeignKey

class User(db.Model):
    __tablename__ = 'user'
    rut = Column(String(12), primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name_father = Column(String(100), nullable=False)
    last_name_mother = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    cafe_id = Column(Integer, ForeignKey('cafe.id'), nullable=False)

    def serialize(self):
        return {
            "rut": self.rut,
            "first_name": self.first_name,
            "last_name_father": self.last_name_father,
            "last_name_mother": self.last_name_mother,
            "username": self.username,
            "email": self.email,
            "role_id": self.role_id,
            "cafe_id": self.cafe_id,
        }
