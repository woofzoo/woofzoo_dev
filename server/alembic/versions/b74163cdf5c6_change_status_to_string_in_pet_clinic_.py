"""change_status_to_string_in_pet_clinic_access

Revision ID: b74163cdf5c6
Revises: bc9dd895956d
Create Date: 2025-10-12 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b74163cdf5c6'
down_revision = 'bc9dd895956d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Change status column from ENUM to String(50)
    # This requires a few steps to handle existing data and enum type
    
    # Step 1: Add a temporary column
    op.add_column('pet_clinic_access', sa.Column('status_new', sa.String(50), nullable=True))
    
    # Step 2: Copy data from old column to new column (cast enum to text)
    op.execute("""
        UPDATE pet_clinic_access 
        SET status_new = status::text
    """)
    
    # Step 3: Drop the old column (this will also drop the enum if no other columns use it)
    op.drop_column('pet_clinic_access', 'status')
    
    # Step 4: Rename the new column to 'status'
    op.alter_column('pet_clinic_access', 'status_new', new_column_name='status')
    
    # Step 5: Set NOT NULL constraint and default value
    op.alter_column('pet_clinic_access', 'status',
                    nullable=False,
                    server_default='active')
    
    # Step 6: Recreate the index
    op.create_index('ix_pet_clinic_access_status', 'pet_clinic_access', ['status'])
    
    # Step 7: Try to drop the enum type if it exists (may fail if other tables use it)
    # Using try/except pattern via raw SQL
    op.execute("""
        DO $$ 
        BEGIN
            DROP TYPE IF EXISTS accessstatus CASCADE;
        EXCEPTION 
            WHEN OTHERS THEN NULL;
        END $$;
    """)


def downgrade() -> None:
    # Downgrade: Convert String back to ENUM
    # This is optional and may not be needed in production
    
    # Step 1: Create the enum type
    access_status_enum = sa.Enum('active', 'expired', 'revoked', name='accessstatus')
    access_status_enum.create(op.get_bind(), checkfirst=True)
    
    # Step 2: Add temporary column with enum type
    op.add_column('pet_clinic_access', 
                  sa.Column('status_enum', access_status_enum, nullable=True))
    
    # Step 3: Copy and cast data
    op.execute("""
        UPDATE pet_clinic_access 
        SET status_enum = status::accessstatus
    """)
    
    # Step 4: Drop the string column
    op.drop_index('ix_pet_clinic_access_status', table_name='pet_clinic_access')
    op.drop_column('pet_clinic_access', 'status')
    
    # Step 5: Rename enum column to 'status'
    op.alter_column('pet_clinic_access', 'status_enum', new_column_name='status')
    
    # Step 6: Set NOT NULL and default
    op.alter_column('pet_clinic_access', 'status',
                    nullable=False,
                    server_default='active')
    
    # Step 7: Recreate index
    op.create_index('ix_pet_clinic_access_status', 'pet_clinic_access', ['status'])
