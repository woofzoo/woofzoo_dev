"""add_access_level_in_invitation

Revision ID: 3bf2106995e4
Revises: b0dec362b9ac
Create Date: 2025-09-28 13:18:41.088885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bf2106995e4'
down_revision = 'b0dec362b9ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('family_invitations', sa.Column('access_level', sa.String(100), nullable=False))


def downgrade() -> None:
    op.drop_column('family_invitations', 'access_level')
