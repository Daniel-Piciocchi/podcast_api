"""Add is_admin column to User

Revision ID: 7c81f1c89e9c
Revises: 2734d721d36a
Create Date: 2023-03-18 10:01:59.452259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c81f1c89e9c'
down_revision = '2734d721d36a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=True))
        batch_op.drop_column('role')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.VARCHAR(length=20), nullable=False))
        batch_op.drop_column('is_admin')

    # ### end Alembic commands ###
