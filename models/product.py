from .base import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .combo_menu_detail import detalle_combo_menu  # Importing the intermediate table

class Product(db.Model):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    
    product_category_id = Column(Integer, ForeignKey('product_category.id'), nullable=False)
    product_category = relationship('ProductCategory', backref='products')
    
    cafe_id = Column(Integer, ForeignKey('cafe.id'), nullable=False)
    cafe = relationship('Cafe', backref='products')
    
    item_type_id = Column(Integer, ForeignKey('item_type.id'), nullable=False)
    item_type = relationship('ItemType')

    combos = relationship('ComboMenu', secondary=detalle_combo_menu, backref='products_in_combo')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "product_category_id": self.product_category_id,
            "cafe_id": self.cafe_id,
            "item_type_id": self.item_type_id,
        }
