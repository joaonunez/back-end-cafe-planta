# models/sale.py
from extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

class Sale(db.Model):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False, default=datetime.now)
    total_amount = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    comments = Column(Text, nullable=True)

    customer_rut = Column(String(12), ForeignKey('customer.rut'), nullable=False)
    cafe_id = Column(Integer, ForeignKey('cafe.id'), nullable=False)
    waiter_rut = Column(String(12), ForeignKey('user.rut'), nullable=True)
    dining_area_id = Column(Integer, ForeignKey('dining_area.id'), nullable=True)

    customer = relationship('Customer')
    cafe = relationship('Cafe')
    waiter = relationship('User')
    dining_area = relationship('DiningArea')

    # Nueva relación con SaleDetail
    details = relationship('SaleDetail', backref='sale', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "total_amount": self.total_amount,
            "status": self.status,
            "comments": self.comments,
            "customer_rut": self.customer_rut,
            "cafe_id": self.cafe_id,
            "waiter_rut": self.waiter_rut,
            "dining_area_id": self.dining_area_id,
        }
