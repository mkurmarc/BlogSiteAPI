"""create posts table

Revision ID: 4d22c6a910a6
Revises: 
Create Date: 2022-07-20 21:38:52.544970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d22c6a910a6'
down_revision = None
branch_labels = None
depends_on = None

# handles the changes
def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


# handles rolling it back
def downgrade() -> None:
    op.drop_table('posts')
    pass
