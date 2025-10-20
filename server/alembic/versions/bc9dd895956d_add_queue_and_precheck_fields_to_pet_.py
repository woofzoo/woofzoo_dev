"""add_queue_and_precheck_fields_to_pet_clinic_access

Revision ID: bc9dd895956d
Revises: 11a7277f2a1a
Create Date: 2025-10-11 15:38:59.599556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc9dd895956d'
down_revision = '11a7277f2a1a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add pre-check vitals fields
    op.add_column('pet_clinic_access', sa.Column('pre_check_weight', sa.Float(), nullable=True))
    op.add_column('pet_clinic_access', sa.Column('pre_check_temperature', sa.Float(), nullable=True))
    op.add_column('pet_clinic_access', sa.Column('pre_check_heart_rate', sa.Integer(), nullable=True))
    op.add_column('pet_clinic_access', sa.Column('pre_check_respiratory_rate', sa.Integer(), nullable=True))
    op.add_column('pet_clinic_access', sa.Column('pre_check_notes', sa.Text(), nullable=True))
    op.add_column('pet_clinic_access', sa.Column('pre_check_completed_at', sa.DateTime(), nullable=True))
    op.add_column('pet_clinic_access', sa.Column('pre_check_by_user_id', sa.UUID(), nullable=True))
    
    # Add queue management fields (using String, not database ENUM)
    op.add_column('pet_clinic_access', sa.Column('queue_status', sa.String(50), nullable=True))
    op.add_column('pet_clinic_access', sa.Column('queue_position', sa.Integer(), nullable=True))
    op.add_column('pet_clinic_access', sa.Column('assigned_to_doctor_at', sa.DateTime(), nullable=True))
    op.add_column('pet_clinic_access', sa.Column('visit_completed_at', sa.DateTime(), nullable=True))
    
    # Add medical record link
    op.add_column('pet_clinic_access', sa.Column('medical_record_id', sa.UUID(), nullable=True))
    
    # Add foreign key for pre_check_by_user_id
    op.create_foreign_key(
        op.f('fk_pet_clinic_access_pre_check_by_user_id_users'),
        'pet_clinic_access', 'users',
        ['pre_check_by_user_id'], ['public_id']
    )
    
    # Add foreign key for medical_record_id
    op.create_foreign_key(
        op.f('fk_pet_clinic_access_medical_record_id_medical_records'),
        'pet_clinic_access', 'medical_records',
        ['medical_record_id'], ['id']
    )
    
    # Create index on queue_status for performance
    op.create_index('idx_pet_clinic_access_queue_status', 'pet_clinic_access', ['queue_status'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_pet_clinic_access_queue_status', table_name='pet_clinic_access')
    
    # Drop foreign keys
    op.drop_constraint(op.f('fk_pet_clinic_access_medical_record_id_medical_records'), 'pet_clinic_access', type_='foreignkey')
    op.drop_constraint(op.f('fk_pet_clinic_access_pre_check_by_user_id_users'), 'pet_clinic_access', type_='foreignkey')
    
    # Drop columns
    op.drop_column('pet_clinic_access', 'medical_record_id')
    op.drop_column('pet_clinic_access', 'visit_completed_at')
    op.drop_column('pet_clinic_access', 'assigned_to_doctor_at')
    op.drop_column('pet_clinic_access', 'queue_position')
    op.drop_column('pet_clinic_access', 'queue_status')
    op.drop_column('pet_clinic_access', 'pre_check_by_user_id')
    op.drop_column('pet_clinic_access', 'pre_check_completed_at')
    op.drop_column('pet_clinic_access', 'pre_check_notes')
    op.drop_column('pet_clinic_access', 'pre_check_respiratory_rate')
    op.drop_column('pet_clinic_access', 'pre_check_heart_rate')
    op.drop_column('pet_clinic_access', 'pre_check_temperature')
    op.drop_column('pet_clinic_access', 'pre_check_weight')
