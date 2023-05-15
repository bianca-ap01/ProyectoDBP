"""empty message

Revision ID: 0063cb117047
Revises: ec65b2f1961c
Create Date: 2023-05-15 00:38:30.426263

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0063cb117047'
down_revision = 'ec65b2f1961c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('users_atcoder_handle_key', type_='unique')
        batch_op.drop_constraint('users_codeforces_handle_key', type_='unique')
        batch_op.drop_constraint('users_vjudge_handle_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_unique_constraint('users_vjudge_handle_key', ['vjudge_handle'])
        batch_op.create_unique_constraint('users_codeforces_handle_key', ['codeforces_handle'])
        batch_op.create_unique_constraint('users_atcoder_handle_key', ['atcoder_handle'])

    # ### end Alembic commands ###