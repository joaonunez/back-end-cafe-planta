from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Time, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
import datetime

db = SQLAlchemy()

# Tabla intermedia para la relación muchos a muchos entre ComboMenu y Producto
detalle_combo_menu = Table('detalle_combo_menu', db.Model.metadata,
    Column('combo_menu_id', Integer, ForeignKey('combo_menu.id'), primary_key=True),
    Column('producto_id', Integer, ForeignKey('producto.id'), primary_key=True)
)

# Tabla intermedia User-Beneficio
user_beneficio = Table('user_beneficio', db.Model.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('beneficio_id', Integer, ForeignKey('beneficio.id'), primary_key=True)
)

# Clase Pais
class Pais(db.Model):
    __tablename__ = 'pais'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    regiones = relationship('Region', backref='pais', lazy=True)

# Clase Region
class Region(db.Model):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    pais_id = Column(Integer, ForeignKey('pais.id'), nullable=False)
    comunas = relationship('Comuna', backref='region', lazy=True)

# Clase Comuna
class Comuna(db.Model):
    __tablename__ = 'comuna'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)

# Clase Rol
class Rol(db.Model):
    __tablename__ = 'rol'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    salario_base = Column(Integer, nullable=False)

# Clase Beneficio
class Beneficio(db.Model):
    __tablename__ = 'beneficio'
    id = Column(Integer, primary_key=True)
    precio = Column(Integer, nullable=False)
    descripcion = Column(String(255), nullable=False)

# Clase User
class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=False)
    rut = Column(String(12), unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    usuario = Column(String(50), unique=True, nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey('rol.id'), nullable=False)
    rol = relationship('Rol', backref='users', lazy=True)
    beneficios = relationship('Beneficio', secondary=user_beneficio, lazy='subquery')
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    cafeteria = relationship('Cafeteria', backref='users', lazy=True)

# Clase Producto
class Producto(db.Model):
    __tablename__ = 'producto'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    categoria_producto_id = Column(Integer, ForeignKey('categoria_producto.id'), nullable=False)
    categoria_producto = relationship('CategoriaProducto', backref='productos', lazy=True)
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    cafeteria = relationship('Cafeteria', backref='productos', lazy=True)
    tipo_item_id = Column(Integer, ForeignKey('tipo_item.id'), nullable=False)
    tipo_item = relationship('TipoItem', backref='productos', lazy=True)

# Clase CategoriaProducto
class CategoriaProducto(db.Model):
    __tablename__ = 'categoria_producto'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)

# Clase ComboMenu
class ComboMenu(db.Model):
    __tablename__ = 'combo_menu'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Integer, nullable=False)
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    cafeteria = relationship('Cafeteria', backref='combos', lazy=True)
    tipo_item_id = Column(Integer, ForeignKey('tipo_item.id'), nullable=False)
    tipo_item = relationship('TipoItem', backref='combos', lazy=True)
    productos = relationship('Producto', secondary=detalle_combo_menu, lazy='subquery')

# Clase Cafeteria
class Cafeteria(db.Model):
    __tablename__ = 'cafeteria'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=False)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    comuna = relationship('Comuna', backref='cafeterias', lazy=True)

# Clase TipoItem
class TipoItem(db.Model):
    __tablename__ = 'tipo_item'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)

# Clase Venta
class Venta(db.Model):
    __tablename__ = 'venta'
    id = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False, default=datetime.date.today)
    hora = Column(Time, nullable=False, default=datetime.datetime.now().time)
    monto_total = Column(Integer, nullable=False)
    estado = Column(String(50), nullable=False, default="pendiente")
    comentarios = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    user = relationship('User', backref='ventas', lazy=True)
    cafeteria = relationship('Cafeteria', backref='ventas', lazy=True)
    detalles = relationship('DetalleVenta', backref='venta', lazy=True)

# Clase DetalleVenta
class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'
    id = Column(Integer, primary_key=True)
    venta_id = Column(Integer, ForeignKey('venta.id'), nullable=False)
    item_id = Column(Integer, nullable=False)
    tipo_item_id = Column(Integer, ForeignKey('tipo_item.id'), nullable=False)
    tipo_item = relationship('TipoItem', backref='detalles', lazy=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Integer, nullable=False)
