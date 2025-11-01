"""add_pet_dob_journal_and_medication_log_tables

Revision ID: 1cbcbc87240d
Revises: b74163cdf5c6
Create Date: 2025-11-01 10:47:46.814674

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '1cbcbc87240d'
down_revision = 'b74163cdf5c6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add date_of_birth column to pets table
    op.add_column('pets', sa.Column('date_of_birth', sa.Date(), nullable=True))
    
    # Create pet_journals table
    op.create_table('pet_journals',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('pet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_by_user_id', sa.Integer(), nullable=False),
        sa.Column('entry_type', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('entry_date', sa.Date(), nullable=False),
        sa.Column('metadata', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id'], name=op.f('fk_pet_journals_created_by_user_id_users')),
        sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name=op.f('fk_pet_journals_pet_id_pets')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_pet_journals'))
    )
    op.create_index(op.f('ix_pet_journals_created_by_user_id'), 'pet_journals', ['created_by_user_id'], unique=False)
    op.create_index(op.f('ix_pet_journals_entry_date'), 'pet_journals', ['entry_date'], unique=False)
    op.create_index(op.f('ix_pet_journals_entry_type'), 'pet_journals', ['entry_type'], unique=False)
    op.create_index(op.f('ix_pet_journals_pet_id'), 'pet_journals', ['pet_id'], unique=False)
    
    # Create medication_logs table
    op.create_table('medication_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('pet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_by_user_id', sa.Integer(), nullable=False),
        sa.Column('medication_name', sa.String(length=200), nullable=False),
        sa.Column('dosage', sa.String(length=100), nullable=False),
        sa.Column('dosage_unit', sa.String(length=50), nullable=False),
        sa.Column('administered_at', sa.DateTime(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id'], name=op.f('fk_medication_logs_created_by_user_id_users')),
        sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name=op.f('fk_medication_logs_pet_id_pets')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_medication_logs'))
    )
    op.create_index(op.f('ix_medication_logs_administered_at'), 'medication_logs', ['administered_at'], unique=False)
    op.create_index(op.f('ix_medication_logs_created_by_user_id'), 'medication_logs', ['created_by_user_id'], unique=False)
    op.create_index(op.f('ix_medication_logs_pet_id'), 'medication_logs', ['pet_id'], unique=False)


def downgrade() -> None:
    # Drop medication_logs table
    op.drop_index(op.f('ix_medication_logs_pet_id'), table_name='medication_logs')
    op.drop_index(op.f('ix_medication_logs_created_by_user_id'), table_name='medication_logs')
    op.drop_index(op.f('ix_medication_logs_administered_at'), table_name='medication_logs')
    op.drop_table('medication_logs')
    
    # Drop pet_journals table
    op.drop_index(op.f('ix_pet_journals_pet_id'), table_name='pet_journals')
    op.drop_index(op.f('ix_pet_journals_entry_type'), table_name='pet_journals')
    op.drop_index(op.f('ix_pet_journals_entry_date'), table_name='pet_journals')
    op.drop_index(op.f('ix_pet_journals_created_by_user_id'), table_name='pet_journals')
    op.drop_table('pet_journals')
    
    # Remove date_of_birth column from pets table
    op.drop_column('pets', 'date_of_birth')
