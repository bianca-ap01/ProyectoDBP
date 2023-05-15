"""empty message

Revision ID: da617951260f
Revises: 4feaa23782fc
Create Date: 2023-05-14 23:13:07.316021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da617951260f'
down_revision = '4feaa23782fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('nickname',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('nickname',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)

    # ### end Alembic commands ###
