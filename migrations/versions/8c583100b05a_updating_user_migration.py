"""Updating user migration.

Revision ID: 8c583100b05a
Revises: 
Create Date: 2021-04-03 16:03:29.936810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c583100b05a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('items')
    op.add_column('user', sa.Column('buget', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'buget')
    op.create_table('items',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=20), nullable=False),
    sa.Column('Price', sa.FLOAT(), nullable=False),
    sa.Column('barcode', sa.VARCHAR(length=12), nullable=False),
    sa.Column('description', sa.VARCHAR(length=1024), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('barcode'),
    sa.UniqueConstraint('description'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###
