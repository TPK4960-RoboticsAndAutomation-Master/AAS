"""empty message

Revision ID: adf1a3728df5
Revises: d19ce263c1c1
Create Date: 2021-04-30 14:33:32.114483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adf1a3728df5'
down_revision = 'd19ce263c1c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('operator', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'operator')
    # ### end Alembic commands ###
