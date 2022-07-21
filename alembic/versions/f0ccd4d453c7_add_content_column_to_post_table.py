"""add content column to post table

Revision ID: f0ccd4d453c7
Revises: 4d22c6a910a6
Create Date: 2022-07-20 21:48:53.498411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0ccd4d453c7'
down_revision = '4d22c6a910a6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
