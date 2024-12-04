from extensions import db
from sqlalchemy import Column, Integer, ForeignKey
from models.product import Product
from models.combo_menu import ComboMenu

class SaleDetail(db.Model):
    __tablename__ = 'sale_detail'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sale_id = Column(Integer, ForeignKey('sale.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Integer, nullable=False)
    item_type_id = Column(Integer, ForeignKey('item_type.id'), nullable=False)
    item_id = Column(Integer, nullable=False)

    def serialize(self):
        if self.item_type_id == 1:  # Combo
            item = ComboMenu.query.get(self.item_id)
        elif self.item_type_id == 2:  # Producto
            item = Product.query.get(self.item_id)
        else:
            item = None

        return {
            "id": self.id,
            "sale_id": self.sale_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "item_type_id": self.item_type_id,
            "item_id": self.item_id,
            "name": item.name if item else "Item desconocido",
            "image_url": item.image_url if item else None,
            "total": self.quantity * self.unit_price,
        }
