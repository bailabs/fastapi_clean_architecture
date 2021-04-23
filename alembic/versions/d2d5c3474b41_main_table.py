"""main_table

Revision ID: d2d5c3474b41
Revises: 
Create Date: 2021-04-22 14:51:43.465380

"""
from alembic import op
from sqlalchemy import Column, String

# revision identifiers, used by Alembic.
revision = '0e449141e48d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'users',
        Column('verification_code', String(200))
    )


def downgrade():
    op.drop_column('users', 'verification_code')
