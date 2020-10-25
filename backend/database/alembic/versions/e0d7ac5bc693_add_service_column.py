"""Add service column

Revision ID: e0d7ac5bc693
Revises: 90fde3e42e28
Create Date: 2020-10-25 09:48:25.306241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0d7ac5bc693'
down_revision = '90fde3e42e28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('service', sa.String(), nullable=True))
    op.create_index(op.f('ix_items_service'), 'items', ['service'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_items_service'), table_name='items')
    op.drop_column('items', 'service')
    # ### end Alembic commands ###
