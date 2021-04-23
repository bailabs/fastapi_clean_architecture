"""empty message

Revision ID: 38e167e43592
Revises: 0e449141e48d
Create Date: 2021-04-22 15:34:43.578813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38e167e43592'
down_revision = '0e449141e48d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_blacklisted_token_auth_token'), 'blacklisted_token', ['auth_token'], unique=False)
    op.create_index(op.f('ix_userinfo_description'), 'userinfo', ['description'], unique=False)
    op.create_index(op.f('ix_userinfo_firstname'), 'userinfo', ['firstname'], unique=False)
    op.create_index(op.f('ix_userinfo_fullname'), 'userinfo', ['fullname'], unique=False)
    op.create_index(op.f('ix_userinfo_id'), 'userinfo', ['id'], unique=False)
    op.create_index(op.f('ix_userinfo_lastname'), 'userinfo', ['lastname'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_identifier'), 'users', ['identifier'], unique=True)
    op.drop_column('users', 'verification_code')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('verification_code', sa.VARCHAR(length=200), nullable=True))
    op.drop_index(op.f('ix_users_identifier'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_userinfo_lastname'), table_name='userinfo')
    op.drop_index(op.f('ix_userinfo_id'), table_name='userinfo')
    op.drop_index(op.f('ix_userinfo_fullname'), table_name='userinfo')
    op.drop_index(op.f('ix_userinfo_firstname'), table_name='userinfo')
    op.drop_index(op.f('ix_userinfo_description'), table_name='userinfo')
    op.drop_index(op.f('ix_blacklisted_token_auth_token'), table_name='blacklisted_token')
    # ### end Alembic commands ###
