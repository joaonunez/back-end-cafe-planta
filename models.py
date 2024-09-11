from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Time, Table, Text, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()

# Clase País
class Pais(db.Model):
    __tablename__ = 'pais'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    regiones = relationship('Region', backref='pais', lazy=True)

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        }

# Clase Región
class Region(db.Model):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    pais_id = Column(Integer, ForeignKey('pais.id'), nullable=False)
    comunas = relationship('Comuna', backref='region', lazy=True)

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "pais_id": self.pais_id,
        }

# Clase Comuna
class Comuna(db.Model):
    __tablename__ = 'comuna'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "region_id": self.region_id,
        }

# Clase Rol
class Rol(db.Model):
    __tablename__ = 'rol'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    salario_base = Column(Integer, nullable=False)

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "salario_base": self.salario_base,
        }

# Clase Beneficio
class Beneficio(db.Model):
    __tablename__ = 'beneficio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    precio = Column(Integer, nullable=False)
    descripcion = Column(String(255), nullable=False)

    def serializar(self):
        return {
            "id": self.id,
            "precio": self.precio,
            "descripcion": self.descripcion,
        }

# Clase Usuario
class Usuario(db.Model):
    __tablename__ = 'usuario'
    rut = Column(String(12), primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=False)
    usuario = Column(String(50), unique=True, nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)

    rol_id = Column(Integer, ForeignKey('rol.id'), nullable=False)
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)

    def serializar(self):
        return {
            "rut": self.rut,
            "nombre": self.nombre,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "usuario": self.usuario,
            "correo": self.correo,
            "rol_id": self.rol_id,
            "cafeteria_id": self.cafeteria_id,
        }

# Clase Cliente
class Cliente(db.Model):
    __tablename__ = 'cliente'
    rut = Column(String(12), primary_key=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    usuario = Column(String(50), unique=True, nullable=False)

    def serializar(self):
        return {
            "rut": self.rut,
            "nombre": self.nombre,
            "correo": self.correo,
            "usuario": self.usuario,
        }

# Clase Favoritos
class Favoritos(db.Model):
    __tablename__ = 'favoritos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_rut = Column(String(12), ForeignKey('cliente.rut'), nullable=False)
    producto_id = Column(Integer, ForeignKey('producto.id'), nullable=False)

    def serializar(self):
        return {
            "id": self.id,
            "cliente_rut": self.cliente_rut,
            "producto_id": self.producto_id,
        }

# Clase HistorialPedidos
class HistorialPedidos(db.Model):
    __tablename__ = 'historial_pedidos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_rut = Column(String(12), ForeignKey('cliente.rut'), nullable=False)
    venta_id = Column(Integer, ForeignKey('venta.id'), nullable=False)

    def serializar(self):
        return {
            "id": self.id,
            "cliente_rut": self.cliente_rut,
            "venta_id": self.venta_id,
        }

# Clase CategoriaProducto
class CategoriaProducto(db.Model):
    __tablename__ = 'categoria_producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        }
    
# Clase Producto
class Producto(db.Model):
    __tablename__ = 'producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    
    # Relaciones con otras tablas
    categoria_producto_id = Column(Integer, ForeignKey('categoria_producto.id'), nullable=False)
    categoria_producto = relationship('CategoriaProducto', backref='productos')
    
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    cafeteria = relationship('Cafeteria', backref='productos')
    
    tipo_item_id = Column(Integer, ForeignKey('tipo_item.id'), nullable=False)
    tipo_item = relationship('TipoItem')

    calificaciones = relationship('CalificacionProducto', backref='producto')

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
            "categoria_producto_id": self.categoria_producto_id,
            "cafeteria_id": self.cafeteria_id,
            "tipo_item_id": self.tipo_item_id,
        }

# Clase ComboMenu
class ComboMenu(db.Model):
    __tablename__ = 'combo_menu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Integer, nullable=False)

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
        }

# Clase Cafetería
class Cafeteria(db.Model):
    __tablename__ = 'cafeteria'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=False)

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "direccion": self.direccion,
        }

# Clase TipoItem
class TipoItem(db.Model):
    __tablename__ = 'tipo_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        }

# Clase Mesa
class Mesa(db.Model):
    __tablename__ = 'mesa'
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer, nullable=False)
    qr_code = Column(String(255), nullable=False)

    def serializar(self):
        return {
            "id": self.id,
            "numero": self.numero,
            "qr_code": self.qr_code,
        }

# Clase Venta
class Venta(db.Model):
    __tablename__ = 'venta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False, default=datetime.now)
    hora = Column(Time, nullable=False)
    monto_total = Column(Integer, nullable=False)
    estado = Column(String(50), nullable=False, default="pendiente")
    comentarios = Column(Text, nullable=True)

    def serializar(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "hora": self.hora,
            "monto_total": self.monto_total,
            "estado": self.estado,
            "comentarios": self.comentarios,
        }

# Clase DetalleVenta
class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    venta_id = Column(Integer, ForeignKey('venta.id'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Integer, nullable=False)

    def serializar(self):
        return {
            "id": self.id,
            "venta_id": self.venta_id,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
        }

# Clase CalificacionProducto
class CalificacionProducto(db.Model):
    __tablename__ = 'calificacion_producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_rut = Column(String(12), ForeignKey('cliente.rut'), nullable=False)
    producto_id = Column(Integer, ForeignKey('producto.id'), nullable=False)
    calificacion = Column(Float, nullable=False)
    fecha = Column(Date, nullable=False, default=datetime.now)

    def serializar(self):
        return {
            "id": self.id,
            "cliente_rut": self.cliente_rut,
            "producto_id": self.producto_id,
            "calificacion": self.calificacion,
            "fecha": self.fecha,
        }
