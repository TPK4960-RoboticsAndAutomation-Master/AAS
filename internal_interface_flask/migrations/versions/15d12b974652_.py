"""empty message

Revision ID: 15d12b974652
Revises: d2810f225612
Create Date: 2021-04-19 13:38:25.854446

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15d12b974652'
down_revision = 'd2810f225612'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('robot', sa.Column('udp_url', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('robot', 'udp_url')
    # ### end Alembic commands ###
