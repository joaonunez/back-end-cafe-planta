"""empty message

Revision ID: f42facb4de68
Revises: 
Create Date: 2024-09-06 08:25:51.211625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f42facb4de68'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('beneficio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('precio', sa.Integer(), nullable=False),
    sa.Column('descripcion', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('categoria_producto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pais',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rol',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=50), nullable=False),
    sa.Column('salario_base', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tipo_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('region',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('pais_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pais_id'], ['pais.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comuna',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('region_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['region_id'], ['region.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cafeteria',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('direccion', sa.String(length=255), nullable=False),
    sa.Column('comuna_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['comuna_id'], ['comuna.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('combo_menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('precio', sa.Integer(), nullable=False),
    sa.Column('cafeteria_id', sa.Integer(), nullable=False),
    sa.Column('tipo_item_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cafeteria_id'], ['cafeteria.id'], ),
    sa.ForeignKeyConstraint(['tipo_item_id'], ['tipo_item.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('producto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('precio', sa.Integer(), nullable=False),
    sa.Column('stock', sa.Integer(), nullable=False),
    sa.Column('categoria_producto_id', sa.Integer(), nullable=False),
    sa.Column('cafeteria_id', sa.Integer(), nullable=False),
    sa.Column('tipo_item_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cafeteria_id'], ['cafeteria.id'], ),
    sa.ForeignKeyConstraint(['categoria_producto_id'], ['categoria_producto.id'], ),
    sa.ForeignKeyConstraint(['tipo_item_id'], ['tipo_item.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('apellido_paterno', sa.String(length=100), nullable=False),
    sa.Column('apellido_materno', sa.String(length=100), nullable=False),
    sa.Column('rut', sa.String(length=12), nullable=False),
    sa.Column('fecha_nacimiento', sa.Date(), nullable=False),
    sa.Column('usuario', sa.String(length=50), nullable=False),
    sa.Column('correo', sa.String(length=100), nullable=False),
    sa.Column('contraseña', sa.String(length=255), nullable=False),
    sa.Column('rol_id', sa.Integer(), nullable=False),
    sa.Column('cafeteria_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cafeteria_id'], ['cafeteria.id'], ),
    sa.ForeignKeyConstraint(['rol_id'], ['rol.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('correo'),
    sa.UniqueConstraint('rut'),
    sa.UniqueConstraint('usuario')
    )
    op.create_table('detalle_combo_menu',
    sa.Column('combo_menu_id', sa.Integer(), nullable=False),
    sa.Column('producto_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['combo_menu_id'], ['combo_menu.id'], ),
    sa.ForeignKeyConstraint(['producto_id'], ['producto.id'], ),
    sa.PrimaryKeyConstraint('combo_menu_id', 'producto_id')
    )
    op.create_table('user_beneficio',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('beneficio_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['beneficio_id'], ['beneficio.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'beneficio_id')
    )
    op.create_table('venta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.Date(), nullable=False),
    sa.Column('hora', sa.Time(), nullable=False),
    sa.Column('monto_total', sa.Integer(), nullable=False),
    sa.Column('estado', sa.String(length=50), nullable=False),
    sa.Column('comentarios', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('cafeteria_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cafeteria_id'], ['cafeteria.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('detalle_venta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('venta_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('tipo_item_id', sa.Integer(), nullable=False),
    sa.Column('cantidad', sa.Integer(), nullable=False),
    sa.Column('precio_unitario', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tipo_item_id'], ['tipo_item.id'], ),
    sa.ForeignKeyConstraint(['venta_id'], ['venta.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('detalle_venta')
    op.drop_table('venta')
    op.drop_table('user_beneficio')
    op.drop_table('detalle_combo_menu')
    op.drop_table('user')
    op.drop_table('producto')
    op.drop_table('combo_menu')
    op.drop_table('cafeteria')
    op.drop_table('comuna')
    op.drop_table('region')
    op.drop_table('tipo_item')
    op.drop_table('rol')
    op.drop_table('pais')
    op.drop_table('categoria_producto')
    op.drop_table('beneficio')
    # ### end Alembic commands ###
