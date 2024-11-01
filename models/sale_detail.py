from extensions import db
from sqlalchemy import Column, Integer, ForeignKey

class SaleDetail(db.Model):
    __tablename__ = 'sale_detail'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sale_id = Column(Integer, ForeignKey('sale.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Integer, nullable=False)
    item_type_id = Column(Integer, ForeignKey('item_type.id'), nullable=False)
    item_id = Column(Integer, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "sale_id": self.sale_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "item_type_id": self.item_type_id,
            "item_id": self.item_id,
        }