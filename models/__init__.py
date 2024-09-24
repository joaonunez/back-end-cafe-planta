# Importa la instancia de db
from .base import db

# Importa todos los modelos
from .beneficio import Beneficio
from .cafeteria import Cafeteria
from .calificacion_producto import CalificacionProducto
from .categoria_producto import CategoriaProducto
from .cliente import Cliente
from .comuna import Comuna
from .detalle_venta import DetalleVenta
from .favoritos import Favoritos
from .mesa import Mesa
from .pais import Pais
from .producto import Producto
from .region import Region
from .rol import Rol
from .tipo_item import TipoItem
from .usuario import Usuario
from .venta import Venta
