"""added column to test

Revision ID: 8e6b6f0752d3
Revises: 335124962fce
Create Date: 2018-02-18 13:12:54.302353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e6b6f0752d3'
down_revision = '335124962fce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test', sa.Column('comment', sa.String(length=1000), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('test', 'comment')
    # ### end Alembic commands ###
