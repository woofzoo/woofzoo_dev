"""remove_column_phone_name_from_family_members

Revision ID: 4cbdf29204ae
Revises: 07bc150fcf04
Create Date: 2025-09-28 12:13:14.682730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4cbdf29204ae'
down_revision = '07bc150fcf04'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('family_members', 'phone_number')
    op.drop_column('family_members', 'name')


def downgrade() -> None:
    op.add_column('family_members', sa.Column('phone_number', sa.String(15), nullable=True))
    op.add_column('family_members', sa.Column('name', sa.String(100), nullable=True))
