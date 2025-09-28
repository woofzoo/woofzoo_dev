"""update_family_invitation_to_use_email

Revision ID: 33fe79a995ba
Revises: 0828064a2c4b
Create Date: 2025-09-21 14:17:51.980265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33fe79a995ba'
down_revision = '0828064a2c4b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add email column to family_invitations table
    op.add_column('family_invitations', sa.Column('invited_email', sa.String(255), nullable=True))
    
    # Add index for email
    op.create_index('ix_family_invitations_invited_email', 'family_invitations', ['invited_email'])
    
    # Update existing records (copy phone to email for now)
    op.execute("UPDATE family_invitations SET invited_email = invited_phone WHERE invited_email IS NULL")
    
    # Make email column non-nullable
    op.alter_column('family_invitations', 'invited_email', nullable=False)
    
    # Drop the old phone column index and column
    op.drop_index('ix_family_invitations_invited_phone', table_name='family_invitations')
    op.drop_column('family_invitations', 'invited_phone')


def downgrade() -> None:
    # Add back phone column
    op.add_column('family_invitations', sa.Column('invited_phone', sa.String(15), nullable=True))
    
    # Add index for phone
    op.create_index('ix_family_invitations_invited_phone', 'family_invitations', ['invited_phone'])
    
    # Update existing records (copy email to phone)
    op.execute("UPDATE family_invitations SET invited_phone = invited_email WHERE invited_phone IS NULL")
    
    # Make phone column non-nullable
    op.alter_column('family_invitations', 'invited_phone', nullable=False)
    
    # Drop the email column index and column
    op.drop_index('ix_family_invitations_invited_email', table_name='family_invitations')
    op.drop_column('family_invitations', 'invited_email')
