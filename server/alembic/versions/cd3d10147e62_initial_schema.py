"""initial_schema

Revision ID: cd3d10147e62
Revises: 
Create Date: 2025-11-01 16:18:41.825315

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'cd3d10147e62'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create OTPs table
    op.create_table('otps',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('phone_number', sa.String(length=15), nullable=False),
        sa.Column('otp_code', sa.String(length=6), nullable=False),
        sa.Column('purpose', sa.String(length=13), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('is_used', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_otps'))
    )
    op.create_index(op.f('ix_otps_phone_number'), 'otps', ['phone_number'], unique=False)
    
    # Create Owners table (legacy - might be removed in future)
    op.create_table('owners',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('phone_number', sa.String(length=15), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_owners'))
    )
    op.create_index(op.f('ix_owners_phone_number'), 'owners', ['phone_number'], unique=True)
    
    # Create Users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('public_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('roles', sa.JSON(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column('email_verification_token', sa.String(length=255), nullable=True),
        sa.Column('email_verification_expires', sa.DateTime(), nullable=True),
        sa.Column('password_reset_token', sa.String(length=255), nullable=True),
        sa.Column('password_reset_expires', sa.DateTime(), nullable=True),
        sa.Column('personalization', sa.JSON(), nullable=False),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_public_id'), 'users', ['public_id'], unique=True)
    op.create_index(op.f('ix_users_phone'), 'users', ['phone'], unique=True)
    op.create_index(op.f('ix_users_email_verification_token'), 'users', ['email_verification_token'], unique=False)
    op.create_index(op.f('ix_users_password_reset_token'), 'users', ['password_reset_token'], unique=False)
    
    # Create Clinic Profiles table
    op.create_table('clinic_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('clinic_name', sa.String(length=200), nullable=False),
        sa.Column('license_number', sa.String(length=100), nullable=False),
        sa.Column('address', sa.Text(), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('operating_hours', sa.JSON(), nullable=False),
        sa.Column('services_offered', sa.JSON(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.public_id'], name=op.f('fk_clinic_profiles_user_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_clinic_profiles'))
    )
    op.create_index(op.f('ix_clinic_profiles_user_id'), 'clinic_profiles', ['user_id'], unique=False)
    op.create_index(op.f('ix_clinic_profiles_license_number'), 'clinic_profiles', ['license_number'], unique=True)
    
    # Create Doctor Profiles table
    op.create_table('doctor_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('license_number', sa.String(length=100), nullable=False),
        sa.Column('specialization', sa.String(length=100), nullable=True),
        sa.Column('years_of_experience', sa.Integer(), nullable=True),
        sa.Column('qualifications', sa.JSON(), nullable=False),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.public_id'], name=op.f('fk_doctor_profiles_user_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_doctor_profiles'))
    )
    op.create_index(op.f('ix_doctor_profiles_user_id'), 'doctor_profiles', ['user_id'], unique=False)
    op.create_index(op.f('ix_doctor_profiles_license_number'), 'doctor_profiles', ['license_number'], unique=True)
    
    # Create Families table
    op.create_table('families',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('admin_owner_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['admin_owner_id'], ['users.public_id'], name=op.f('fk_families_admin_owner_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_families'))
    )
    op.create_index(op.f('ix_families_admin_owner_id'), 'families', ['admin_owner_id'], unique=False)
    
    # Create Pets table
    op.create_table('pets',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('pet_id', sa.String(length=50), nullable=False),
        sa.Column('owner_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('pet_type', sa.String(length=20), nullable=False),
        sa.Column('breed', sa.String(length=50), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('gender', sa.String(length=7), nullable=False),
        sa.Column('weight', sa.Float(), nullable=True),
        sa.Column('photos', sa.JSON(), nullable=False),
        sa.Column('emergency_contacts', sa.JSON(), nullable=False),
        sa.Column('insurance_info', sa.JSON(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.public_id'], name=op.f('fk_pets_owner_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_pets'))
    )
    op.create_index(op.f('ix_pets_owner_id'), 'pets', ['owner_id'], unique=False)
    op.create_index(op.f('ix_pets_pet_id'), 'pets', ['pet_id'], unique=True)
    
    # Create Doctor-Clinic Associations table
    op.create_table('doctor_clinic_associations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('doctor_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('clinic_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('employment_type', sa.String(length=10), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('joined_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.id'], name=op.f('fk_doctor_clinic_associations_doctor_id_doctor_profiles')),
        sa.ForeignKeyConstraint(['clinic_id'], ['clinic_profiles.id'], name=op.f('fk_doctor_clinic_associations_clinic_id_clinic_profiles')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_doctor_clinic_associations')),
        sa.UniqueConstraint('doctor_id', 'clinic_id', name='uq_doctor_clinic')
    )
    op.create_index(op.f('ix_doctor_clinic_associations_doctor_id'), 'doctor_clinic_associations', ['doctor_id'], unique=False)
    op.create_index(op.f('ix_doctor_clinic_associations_clinic_id'), 'doctor_clinic_associations', ['clinic_id'], unique=False)
    
    # Create Family Invitations table
    op.create_table('family_invitations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('family_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('invited_email', sa.String(length=255), nullable=False),
        sa.Column('invited_name', sa.String(length=100), nullable=False),
        sa.Column('invited_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('invite_code', sa.String(length=200), nullable=False),
        sa.Column('access_level', sa.String(length=100), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('is_accepted', sa.Boolean(), nullable=False),
        sa.Column('accepted_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['family_id'], ['families.id'], name=op.f('fk_family_invitations_family_id_families')),
        sa.ForeignKeyConstraint(['invited_by'], ['users.public_id'], name=op.f('fk_family_invitations_invited_by_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_family_invitations'))
    )
    op.create_index(op.f('ix_family_invitations_invite_code'), 'family_invitations', ['invite_code'], unique=True)
    
    # Create Family Members table
    op.create_table('family_members',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('family_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('access_level', sa.String(length=9), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('joined_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['family_id'], ['families.id'], name=op.f('fk_family_members_family_id_families')),
        sa.ForeignKeyConstraint(['user_id'], ['users.public_id'], name=op.f('fk_family_members_user_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_family_members'))
    )
    op.create_index(op.f('ix_family_members_family_id'), 'family_members', ['family_id'], unique=False)
    op.create_index(op.f('ix_family_members_user_id'), 'family_members', ['user_id'], unique=False)
    
    # Create Photos table
    op.create_table('photos',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('pet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('mime_type', sa.String(length=100), nullable=False),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('is_primary', sa.Boolean(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('uploaded_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name=op.f('fk_photos_pet_id_pets')),
        sa.ForeignKeyConstraint(['uploaded_by'], ['users.public_id'], name=op.f('fk_photos_uploaded_by_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_photos'))
    )
    op.create_index(op.f('ix_photos_pet_id'), 'photos', ['pet_id'], unique=False)
    
    # Create Pet Clinic Access table
    op.create_table('pet_clinic_access',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('pet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('clinic_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('doctor_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('owner_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('access_granted_at', sa.DateTime(), nullable=False),
        sa.Column('access_expires_at', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(length=7), nullable=False),
        sa.Column('otp_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('purpose', sa.String(length=200), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name=op.f('fk_pet_clinic_access_pet_id_pets')),
        sa.ForeignKeyConstraint(['clinic_id'], ['clinic_profiles.id'], name=op.f('fk_pet_clinic_access_clinic_id_clinic_profiles')),
        sa.ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.id'], name=op.f('fk_pet_clinic_access_doctor_id_doctor_profiles')),
        sa.ForeignKeyConstraint(['owner_id'], ['users.public_id'], name=op.f('fk_pet_clinic_access_owner_id_users')),
        sa.ForeignKeyConstraint(['otp_id'], ['otps.id'], name=op.f('fk_pet_clinic_access_otp_id_otps')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_pet_clinic_access'))
    )
    op.create_index(op.f('ix_pet_clinic_access_pet_id'), 'pet_clinic_access', ['pet_id'], unique=False)
    op.create_index(op.f('ix_pet_clinic_access_clinic_id'), 'pet_clinic_access', ['clinic_id'], unique=False)
    
    # Create Allergies table
    op.create_table('allergies',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('pet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('allergen', sa.String(length=200), nullable=False),
        sa.Column('allergy_type', sa.String(length=13), nullable=False),
        sa.Column('severity', sa.String(length=16), nullable=False),
        sa.Column('symptoms', sa.JSON(), nullable=False),
        sa.Column('reaction_description', sa.Text(), nullable=True),
        sa.Column('diagnosed_by_doctor_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('diagnosed_date', sa.Date(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_by_user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name=op.f('fk_allergies_pet_id_pets')),
        sa.ForeignKeyConstraint(['diagnosed_by_doctor_id'], ['doctor_profiles.id'], name=op.f('fk_allergies_diagnosed_by_doctor_id_doctor_profiles')),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['users.public_id'], name=op.f('fk_allergies_created_by_user_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_allergies'))
    )
    op.create_index(op.f('ix_allergies_pet_id'), 'allergies', ['pet_id'], unique=False)
    
    # Create Medical Records table
    op.create_table('medical_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('pet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('visit_date', sa.DateTime(), nullable=False),
        sa.Column('clinic_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('doctor_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('visit_type', sa.String(length=15), nullable=False),
        sa.Column('chief_complaint', sa.Text(), nullable=True),
        sa.Column('diagnosis', sa.Text(), nullable=True),
        sa.Column('symptoms', sa.JSON(), nullable=False),
        sa.Column('treatment_plan', sa.Text(), nullable=True),
        sa.Column('clinical_notes', sa.Text(), nullable=True),
        sa.Column('weight', sa.Float(), nullable=True),
        sa.Column('temperature', sa.Float(), nullable=True),
        sa.Column('vital_signs', sa.JSON(), nullable=False),
        sa.Column('follow_up_required', sa.Boolean(), nullable=False),
        sa.Column('follow_up_date', sa.Date(), nullable=True),
        sa.Column('follow_up_notes', sa.Text(), nullable=True),
        sa.Column('is_emergency', sa.Boolean(), nullable=False),
        sa.Column('created_by_user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_by_role', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name=op.f('fk_medical_records_pet_id_pets')),
        sa.ForeignKeyConstraint(['clinic_id'], ['clinic_profiles.id'], name=op.f('fk_medical_records_clinic_id_clinic_profiles')),
        sa.ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.id'], name=op.f('fk_medical_records_doctor_id_doctor_profiles')),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['users.public_id'], name=op.f('fk_medical_records_created_by_user_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_medical_records'))
    )
    op.create_index(op.f('ix_medical_records_pet_id'), 'medical_records', ['pet_id'], unique=False)
    op.create_index(op.f('ix_medical_records_visit_date'), 'medical_records', ['visit_date'], unique=False)
    
    # Create Pet Journals table
    op.create_table('pet_journals',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('pet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_by_user_id', sa.Integer(), nullable=False),
        sa.Column('entry_type', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('entry_date', sa.Date(), nullable=False),
        sa.Column('details', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name=op.f('fk_pet_journals_pet_id_pets')),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id'], name=op.f('fk_pet_journals_created_by_user_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_pet_journals'))
    )
    op.create_index(op.f('ix_pet_journals_pet_id'), 'pet_journals', ['pet_id'], unique=False)
    op.create_index(op.f('ix_pet_journals_entry_date'), 'pet_journals', ['entry_date'], unique=False)
    op.create_index(op.f('ix_pet_journals_entry_type'), 'pet_journals', ['entry_type'], unique=False)
    op.create_index(op.f('ix_pet_journals_created_by_user_id'), 'pet_journals', ['created_by_user_id'], unique=False)
    
    # Create Medication Logs table
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
        sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name=op.f('fk_medication_logs_pet_id_pets')),
        sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id'], name=op.f('fk_medication_logs_created_by_user_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_medication_logs'))
    )
    op.create_index(op.f('ix_medication_logs_pet_id'), 'medication_logs', ['pet_id'], unique=False)
    op.create_index(op.f('ix_medication_logs_administered_at'), 'medication_logs', ['administered_at'], unique=False)
    op.create_index(op.f('ix_medication_logs_created_by_user_id'), 'medication_logs', ['created_by_user_id'], unique=False)
    
    # Create Prescriptions table
    op.create_table('prescriptions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('medical_record_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('pet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('medication_name', sa.String(length=200), nullable=False),
        sa.Column('dosage', sa.String(length=100), nullable=False),
        sa.Column('dosage_unit', sa.String(length=50), nullable=False),
        sa.Column('frequency', sa.String(length=100), nullable=False),
        sa.Column('route', sa.String(length=50), nullable=False),
        sa.Column('duration', sa.String(length=100), nullable=False),
        sa.Column('instructions', sa.Text(), nullable=True),
        sa.Column('prescribed_by_doctor_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('prescribed_date', sa.Date(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('refills_allowed', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['medical_record_id'], ['medical_records.id'], name=op.f('fk_prescriptions_medical_record_id_medical_records')),
        sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name=op.f('fk_prescriptions_pet_id_pets')),
        sa.ForeignKeyConstraint(['prescribed_by_doctor_id'], ['doctor_profiles.id'], name=op.f('fk_prescriptions_prescribed_by_doctor_id_doctor_profiles')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_prescriptions'))
    )
    op.create_index(op.f('ix_prescriptions_pet_id'), 'prescriptions', ['pet_id'], unique=False)
    op.create_index(op.f('ix_prescriptions_medical_record_id'), 'prescriptions', ['medical_record_id'], unique=False)
    
    # Create Lab Tests table
    op.create_table('lab_tests',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('medical_record_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('pet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('test_name', sa.String(length=200), nullable=False),
        sa.Column('test_type', sa.String(length=100), nullable=False),
        sa.Column('ordered_by_doctor_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ordered_at', sa.DateTime(), nullable=False),
        sa.Column('performed_at', sa.DateTime(), nullable=True),
        sa.Column('performed_by_clinic_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('status', sa.String(length=11), nullable=False),
        sa.Column('results', sa.Text(), nullable=True),
        sa.Column('results_json', sa.JSON(), nullable=False),
        sa.Column('results_file_url', sa.String(length=500), nullable=True),
        sa.Column('reference_ranges', sa.JSON(), nullable=False),
        sa.Column('abnormal_flags', sa.JSON(), nullable=False),
        sa.Column('interpretation', sa.Text(), nullable=True),
        sa.Column('is_abnormal', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['medical_record_id'], ['medical_records.id'], name=op.f('fk_lab_tests_medical_record_id_medical_records')),
        sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name=op.f('fk_lab_tests_pet_id_pets')),
        sa.ForeignKeyConstraint(['ordered_by_doctor_id'], ['doctor_profiles.id'], name=op.f('fk_lab_tests_ordered_by_doctor_id_doctor_profiles')),
        sa.ForeignKeyConstraint(['performed_by_clinic_id'], ['clinic_profiles.id'], name=op.f('fk_lab_tests_performed_by_clinic_id_clinic_profiles')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_lab_tests'))
    )
    op.create_index(op.f('ix_lab_tests_pet_id'), 'lab_tests', ['pet_id'], unique=False)
    op.create_index(op.f('ix_lab_tests_medical_record_id'), 'lab_tests', ['medical_record_id'], unique=False)
    
    # Create Vaccinations table
    op.create_table('vaccinations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('pet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('medical_record_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('vaccine_name', sa.String(length=200), nullable=False),
        sa.Column('vaccine_type', sa.String(length=100), nullable=False),
        sa.Column('manufacturer', sa.String(length=200), nullable=True),
        sa.Column('batch_number', sa.String(length=100), nullable=True),
        sa.Column('administered_by_doctor_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('administered_at', sa.DateTime(), nullable=False),
        sa.Column('administration_site', sa.String(length=100), nullable=True),
        sa.Column('clinic_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('next_due_date', sa.Date(), nullable=True),
        sa.Column('is_booster', sa.Boolean(), nullable=False),
        sa.Column('reaction_notes', sa.Text(), nullable=True),
        sa.Column('certificate_url', sa.String(length=500), nullable=True),
        sa.Column('is_required_by_law', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name=op.f('fk_vaccinations_pet_id_pets')),
        sa.ForeignKeyConstraint(['medical_record_id'], ['medical_records.id'], name=op.f('fk_vaccinations_medical_record_id_medical_records')),
        sa.ForeignKeyConstraint(['administered_by_doctor_id'], ['doctor_profiles.id'], name=op.f('fk_vaccinations_administered_by_doctor_id_doctor_profiles')),
        sa.ForeignKeyConstraint(['clinic_id'], ['clinic_profiles.id'], name=op.f('fk_vaccinations_clinic_id_clinic_profiles')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_vaccinations'))
    )
    op.create_index(op.f('ix_vaccinations_pet_id'), 'vaccinations', ['pet_id'], unique=False)
    op.create_index(op.f('ix_vaccinations_medical_record_id'), 'vaccinations', ['medical_record_id'], unique=False)
    
    # Create Medical Record Attachments table
    op.create_table('medical_record_attachments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('medical_record_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('lab_test_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('vaccination_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('pet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('file_name', sa.String(length=255), nullable=False),
        sa.Column('file_url', sa.String(length=500), nullable=False),
        sa.Column('file_type', sa.String(length=50), nullable=False),
        sa.Column('file_size', sa.BigInteger(), nullable=False),
        sa.Column('attachment_type', sa.String(length=11), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('uploaded_by_user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('uploaded_by_role', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['medical_record_id'], ['medical_records.id'], name=op.f('fk_medical_record_attachments_medical_record_id_medical_records')),
        sa.ForeignKeyConstraint(['lab_test_id'], ['lab_tests.id'], name=op.f('fk_medical_record_attachments_lab_test_id_lab_tests')),
        sa.ForeignKeyConstraint(['vaccination_id'], ['vaccinations.id'], name=op.f('fk_medical_record_attachments_vaccination_id_vaccinations')),
        sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name=op.f('fk_medical_record_attachments_pet_id_pets')),
        sa.ForeignKeyConstraint(['uploaded_by_user_id'], ['users.public_id'], name=op.f('fk_medical_record_attachments_uploaded_by_user_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_medical_record_attachments'))
    )
    op.create_index(op.f('ix_medical_record_attachments_pet_id'), 'medical_record_attachments', ['pet_id'], unique=False)


def downgrade() -> None:
    # Drop all tables in reverse order (respecting foreign key dependencies)
    op.drop_table('medical_record_attachments')
    op.drop_table('vaccinations')
    op.drop_table('lab_tests')
    op.drop_table('prescriptions')
    op.drop_table('medication_logs')
    op.drop_table('pet_journals')
    op.drop_table('medical_records')
    op.drop_table('allergies')
    op.drop_table('pet_clinic_access')
    op.drop_table('photos')
    op.drop_table('family_members')
    op.drop_table('family_invitations')
    op.drop_table('doctor_clinic_associations')
    op.drop_table('pets')
    op.drop_table('families')
    op.drop_table('doctor_profiles')
    op.drop_table('clinic_profiles')
    op.drop_table('users')
    op.drop_table('owners')
    op.drop_table('otps')
