"""empty message

Revision ID: 5f5121196fe6
Revises: 
Create Date: 2018-02-27 10:55:21.680600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f5121196fe6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('documents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('doc_path', sa.String(length=500), nullable=True),
    sa.Column('doc_name', sa.String(length=100), nullable=True),
    sa.Column('api_number', sa.String(length=12), nullable=True),
    sa.Column('test_date', sa.Date(), nullable=True),
    sa.Column('init_bradenhead_pressure', sa.REAL(), nullable=True),
    sa.Column('init_intermediate_1_pressure', sa.REAL(), nullable=True),
    sa.Column('init_intermediate_2_pressure', sa.REAL(), nullable=True),
    sa.Column('init_casing_pressure', sa.REAL(), nullable=True),
    sa.Column('init_tubing_pressure', sa.REAL(), nullable=True),
    sa.Column('fin_bradenhead_pressure', sa.REAL(), nullable=True),
    sa.Column('fin_intermediate_1_pressure', sa.REAL(), nullable=True),
    sa.Column('fin_intermediate_2_pressure', sa.REAL(), nullable=True),
    sa.Column('fin_casing_pressure', sa.REAL(), nullable=True),
    sa.Column('fin_tubing_pressure', sa.REAL(), nullable=True),
    sa.Column('bradenhead_buildup_pressure', sa.REAL(), nullable=True),
    sa.Column('intermediate_1_buildup_pressure', sa.REAL(), nullable=True),
    sa.Column('intermediate_2_buildup_pressure', sa.REAL(), nullable=True),
    sa.Column('comment', sa.String(length=1000), nullable=True),
    sa.Column('shut_in', sa.Boolean(), nullable=True),
    sa.Column('water_flow', sa.Boolean(), nullable=True),
    sa.Column('oil_flow', sa.Boolean(), nullable=True),
    sa.Column('scraped', sa.Boolean(), nullable=True),
    sa.Column('scraper_name', sa.String(length=64), nullable=True),
    sa.Column('scraper_id', sa.Integer(), nullable=True),
    sa.Column('date_scraped', sa.Date(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('in_use', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['scraper_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documents_api_number'), 'documents', ['api_number'], unique=False)
    op.create_index(op.f('ix_documents_doc_name'), 'documents', ['doc_name'], unique=True)
    op.create_index(op.f('ix_documents_doc_path'), 'documents', ['doc_path'], unique=True)
    op.create_table('prev_doc',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('doc_id', sa.Integer(), nullable=True),
    sa.Column('doc_path', sa.String(length=500), nullable=True),
    sa.Column('doc_name', sa.String(length=100), nullable=True),
    sa.Column('api_number', sa.String(length=12), nullable=True),
    sa.Column('test_date', sa.Date(), nullable=True),
    sa.Column('init_bradenhead_pressure', sa.REAL(), nullable=True),
    sa.Column('init_intermediate_1_pressure', sa.REAL(), nullable=True),
    sa.Column('init_intermediate_2_pressure', sa.REAL(), nullable=True),
    sa.Column('init_casing_pressure', sa.REAL(), nullable=True),
    sa.Column('init_tubing_pressure', sa.REAL(), nullable=True),
    sa.Column('fin_bradenhead_pressure', sa.REAL(), nullable=True),
    sa.Column('fin_intermediate_1_pressure', sa.REAL(), nullable=True),
    sa.Column('fin_intermediate_2_pressure', sa.REAL(), nullable=True),
    sa.Column('fin_casing_pressure', sa.REAL(), nullable=True),
    sa.Column('fin_tubing_pressure', sa.REAL(), nullable=True),
    sa.Column('bradenhead_buildup_pressure', sa.REAL(), nullable=True),
    sa.Column('intermediate_1_buildup_pressure', sa.REAL(), nullable=True),
    sa.Column('intermediate_2_buildup_pressure', sa.REAL(), nullable=True),
    sa.Column('comment', sa.String(length=1000), nullable=True),
    sa.Column('shut_in', sa.Boolean(), nullable=True),
    sa.Column('water_flow', sa.Boolean(), nullable=True),
    sa.Column('oil_flow', sa.Boolean(), nullable=True),
    sa.Column('scraped', sa.Boolean(), nullable=True),
    sa.Column('scraper_id', sa.Integer(), nullable=True),
    sa.Column('scraper_name', sa.String(length=64), nullable=True),
    sa.Column('date_scraped', sa.Date(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('in_use', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['scraper_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_prev_doc_api_number'), 'prev_doc', ['api_number'], unique=False)
    op.create_index(op.f('ix_prev_doc_doc_name'), 'prev_doc', ['doc_name'], unique=True)
    op.create_index(op.f('ix_prev_doc_doc_path'), 'prev_doc', ['doc_path'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_prev_doc_doc_path'), table_name='prev_doc')
    op.drop_index(op.f('ix_prev_doc_doc_name'), table_name='prev_doc')
    op.drop_index(op.f('ix_prev_doc_api_number'), table_name='prev_doc')
    op.drop_table('prev_doc')
    op.drop_index(op.f('ix_documents_doc_path'), table_name='documents')
    op.drop_index(op.f('ix_documents_doc_name'), table_name='documents')
    op.drop_index(op.f('ix_documents_api_number'), table_name='documents')
    op.drop_table('documents')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###