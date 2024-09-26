from .base import db
from sqlalchemy import Column, Integer, ForeignKey, Table

# Definir la tabla intermedia detalle_combo_menu
detalle_combo_menu = Table(
    'detalle_combo_menu', db.metadata,
    Column('combo_menu_id', Integer, ForeignKey('combo_menu.id'), primary_key=True, nullable=False),
    Column('producto_id', Integer, ForeignKey('producto.id'), primary_key=True, nullable=False),
    Column('cantidad', Integer, nullable=False)  
)
