"""added img_url to exercise

Revision ID: 939df1cd3a9a
Revises: e4ff3bda35cc
Create Date: 2025-03-14 12:36:00.297275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '939df1cd3a9a'
down_revision = 'e4ff3bda35cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exercise', schema=None) as batch_op:
        batch_op.add_column(sa.Column('img_url', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exercise', schema=None) as batch_op:
        batch_op.drop_column('img_url')

    # ### end Alembic commands ###
