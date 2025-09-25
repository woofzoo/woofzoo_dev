"""add_phone_uniqueness_constraint_to_users

Revision ID: 0a393ca192dd
Revises: 33fe79a995ba
Create Date: 2025-09-21 16:39:36.528142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a393ca192dd'
down_revision = '33fe79a995ba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # First, remove any duplicate phone numbers (keep the first one, remove others)
    # This is a safety measure in case there are already duplicates
    op.execute("""
        DELETE FROM users 
        WHERE id NOT IN (
            SELECT MIN(id) 
            FROM users 
            WHERE phone IS NOT NULL 
            GROUP BY phone
        )
        AND phone IS NOT NULL
    """)
    
    # Add unique constraint to phone column
    op.create_unique_constraint('uq_users_phone', 'users', ['phone'])


def downgrade() -> None:
    # Remove the unique constraint
    op.drop_constraint('uq_users_phone', 'users', type_='unique')
