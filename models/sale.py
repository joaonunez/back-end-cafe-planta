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

    details = relationship('SaleDetail', backref='sale', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "total_amount": self.total_amount,
            "status": self.status,
            "comments": self.comments,
            "customer_rut": self.customer_rut,
            "customer_name": self.customer.name if self.customer else "Aún sin asignar",
            "cafe_id": self.cafe_id,
            "cafe_name": self.cafe.name if self.cafe else "Aún sin asignar",
            "waiter_rut": self.waiter_rut,
            "waiter_name": f"{self.waiter.first_name} {self.waiter.last_name_father}" if self.waiter else "Aún sin asignar",
            "dining_area_id": self.dining_area_id,
            "dining_area_number": self.dining_area.number
        }
