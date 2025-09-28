"""update_column_length_for_invite_code

Revision ID: b0dec362b9ac
Revises: 4cbdf29204ae
Create Date: 2025-09-28 12:42:50.504121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0dec362b9ac'
down_revision = '4cbdf29204ae'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('family_invitations', 'invite_code', type_=sa.String(200), nullable=False)


def downgrade() -> None:
    op.alter_column('family_invitations', 'invite_code', type_=sa.String(10), nullable=False)
