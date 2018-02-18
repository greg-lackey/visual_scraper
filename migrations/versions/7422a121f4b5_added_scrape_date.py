"""added scrape date

Revision ID: 7422a121f4b5
Revises: 8e6b6f0752d3
Create Date: 2018-02-18 13:46:27.851322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7422a121f4b5'
down_revision = '8e6b6f0752d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test', sa.Column('date_scraped', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('test', 'date_scraped')
    # ### end Alembic commands ###
