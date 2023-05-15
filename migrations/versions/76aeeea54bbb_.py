"""empty message

Revision ID: 76aeeea54bbb
Revises: da617951260f
Create Date: 2023-05-14 23:21:39.590020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76aeeea54bbb'
down_revision = 'da617951260f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_contest')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_contest',
    sa.Column('user_id', sa.VARCHAR(length=36), autoincrement=False, nullable=True),
    sa.Column('contest_id', sa.VARCHAR(length=36), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['contest_id'], ['contests.id'], name='user_contest_contest_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_contest_user_id_fkey')
    )
    # ### end Alembic commands ###