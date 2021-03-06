"""empty message

Revision ID: 99e7c292ab94
Revises: 74a1f4896bcf
Create Date: 2019-07-30 20:39:42.639294

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '99e7c292ab94'
down_revision = '74a1f4896bcf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alarm', sa.Column('result_1', sa.Float(), nullable=True))
    op.add_column('alarm', sa.Column('result_2', sa.Float(), nullable=True))
    op.add_column('alarm', sa.Column('result_3', sa.Float(), nullable=True))
    op.add_column('alarm', sa.Column('result_4', sa.Float(), nullable=True))
    op.create_foreign_key(None, 'alarm', 'user', ['author_id'], ['id'])
    op.drop_column('alarm', 'result')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alarm', sa.Column('result', mysql.VARCHAR(length=200), nullable=True))
    op.drop_constraint(None, 'alarm', type_='foreignkey')
    op.drop_column('alarm', 'result_4')
    op.drop_column('alarm', 'result_3')
    op.drop_column('alarm', 'result_2')
    op.drop_column('alarm', 'result_1')
    # ### end Alembic commands ###
