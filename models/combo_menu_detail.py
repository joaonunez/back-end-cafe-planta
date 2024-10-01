from .base import db
from sqlalchemy import Column, Integer, ForeignKey, Table

# Define the intermediate table combo_menu_detail
combo_menu_detail = Table(
    'combo_menu_detail', db.metadata,
    Column('combo_menu_id', Integer, ForeignKey('combo_menu.id'), primary_key=True, nullable=False),
    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True, nullable=False),
    Column('quantity', Integer, nullable=False)
)
