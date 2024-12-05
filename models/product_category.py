from extensions import db

from sqlalchemy import Column, Integer, String

class ProductCategory(db.Model):
    __tablename__ = 'product_category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
