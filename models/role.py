from extensions import db

from sqlalchemy import Column, Integer, String

class Role(db.Model):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    base_salary = Column(Integer, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "base_salary": self.base_salary,
        }
