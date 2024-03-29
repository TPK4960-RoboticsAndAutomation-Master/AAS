"""empty message

Revision ID: a789f120e30a
Revises: 15d12b974652
Create Date: 2021-04-20 10:38:39.937791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a789f120e30a'
down_revision = '15d12b974652'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stream_port',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('available_port', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stream_port')
    # ### end Alembic commands ###
