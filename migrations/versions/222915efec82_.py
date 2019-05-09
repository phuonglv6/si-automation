"""empty message

Revision ID: 222915efec82
Revises: 
Create Date: 2019-05-09 17:09:32.762139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '222915efec82'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('doc',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('dated', sa.DateTime(), nullable=True),
    sa.Column('template', sa.String(length=255), nullable=True),
    sa.Column('bkg_no', sa.String(length=255), nullable=True),
    sa.Column('shipper', sa.String(length=255), nullable=True),
    sa.Column('consignee', sa.String(length=255), nullable=True),
    sa.Column('notify', sa.String(length=255), nullable=True),
    sa.Column('also_notify', sa.String(length=255), nullable=True),
    sa.Column('vessel', sa.String(length=255), nullable=True),
    sa.Column('voyage', sa.String(length=255), nullable=True),
    sa.Column('place_of_receipt', sa.String(length=255), nullable=True),
    sa.Column('port_of_loading', sa.String(length=255), nullable=True),
    sa.Column('port_of_discharge', sa.String(length=255), nullable=True),
    sa.Column('place_of_delivery', sa.String(length=255), nullable=True),
    sa.Column('final_destination', sa.String(length=255), nullable=True),
    sa.Column('total_mark', sa.String(length=255), nullable=True),
    sa.Column('total_type', sa.String(length=255), nullable=True),
    sa.Column('total_packages', sa.String(length=255), nullable=True),
    sa.Column('description_of_goods', sa.String(length=255), nullable=True),
    sa.Column('total_weight', sa.String(length=255), nullable=True),
    sa.Column('total_measurement', sa.String(length=255), nullable=True),
    sa.Column('hs_code', sa.String(length=255), nullable=True),
    sa.Column('ams_scac_code', sa.String(length=255), nullable=True),
    sa.Column('aci_code', sa.String(length=255), nullable=True),
    sa.Column('bl_type', sa.String(length=255), nullable=True),
    sa.Column('payment', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('container_detail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('container_no', sa.String(length=255), nullable=True),
    sa.Column('seal_no', sa.String(length=255), nullable=True),
    sa.Column('container_type', sa.String(length=255), nullable=True),
    sa.Column('packages', sa.String(length=255), nullable=True),
    sa.Column('container_mark', sa.String(length=255), nullable=True),
    sa.Column('container_weight', sa.String(length=255), nullable=True),
    sa.Column('container_cbm', sa.String(length=255), nullable=True),
    sa.Column('doc_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['doc_id'], ['doc.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('container_detail')
    op.drop_table('doc')
    # ### end Alembic commands ###