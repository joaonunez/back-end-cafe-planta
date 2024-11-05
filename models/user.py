from extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

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

    # Relación con el modelo Role para obtener el nombre del rol
    role = relationship("Role", backref="users")

    def serialize(self):
        return {
            "rut": self.rut,
            "first_name": self.first_name,
            "last_name_father": self.last_name_father,
            "last_name_mother": self.last_name_mother,
            "username": self.username,
            "email": self.email,
            "role_id": self.role_id,
            "role_name": self.role.name,  # Agrega el nombre del rol en el JSON serializado
            "cafe_id": self.cafe_id,
        }
