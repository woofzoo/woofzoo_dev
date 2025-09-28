"""adding user_id in family-members table

Revision ID: 07bc150fcf04
Revises: 5ac5101233c1
Create Date: 2025-09-28 12:08:16.787639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07bc150fcf04'
down_revision = '5ac5101233c1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('family_members', sa.Column('user_id', sa.UUID(), nullable=False))


def downgrade() -> None:
    op.drop_column('family_members', 'user_id')
