"""repoint_family_and_photo_fks_to_users_public_id

Revision ID: 5ac5101233c1
Revises: 0e78ea37cb0a
Create Date: 2025-09-25 19:05:34.934443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ac5101233c1'
down_revision = '0e78ea37cb0a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # families.admin_owner_id: owners.id -> users.public_id
    op.drop_constraint(op.f('fk_families_admin_owner_id_owners'), 'families', type_='foreignkey')
    op.create_foreign_key(op.f('fk_families_admin_owner_id_users'), 'families', 'users', ['admin_owner_id'], ['public_id'])

    # family_invitations.invited_by: owners.id -> users.public_id
    op.drop_constraint(op.f('fk_family_invitations_invited_by_owners'), 'family_invitations', type_='foreignkey')
    op.create_foreign_key(op.f('fk_family_invitations_invited_by_users'), 'family_invitations', 'users', ['invited_by'], ['public_id'])

    # photos.uploaded_by: users.id (int) -> users.public_id (UUID)
    # Drop existing FK if present; then alter column type to UUID and create new FK
    try:
        op.drop_constraint(op.f('fk_photos_uploaded_by_users'), 'photos', type_='foreignkey')
    except Exception:
        pass
    # Null out values to avoid cast errors, then alter column type
    op.execute("UPDATE photos SET uploaded_by = NULL")
    op.alter_column('photos', 'uploaded_by',
                    existing_type=sa.Integer(),
                    type_=sa.UUID(),
                    postgresql_using='NULL::uuid',
                    nullable=True)
    op.create_foreign_key(op.f('fk_photos_uploaded_by_users'), 'photos', 'users', ['uploaded_by'], ['public_id'])


def downgrade() -> None:
    # Revert families.admin_owner_id back to owners.id
    op.drop_constraint(op.f('fk_families_admin_owner_id_users'), 'families', type_='foreignkey')
    op.create_foreign_key(op.f('fk_families_admin_owner_id_owners'), 'families', 'owners', ['admin_owner_id'], ['id'])

    # Revert family_invitations.invited_by back to owners.id
    op.drop_constraint(op.f('fk_family_invitations_invited_by_users'), 'family_invitations', type_='foreignkey')
    op.create_foreign_key(op.f('fk_family_invitations_invited_by_owners'), 'family_invitations', 'owners', ['invited_by'], ['id'])

    # Revert photos.uploaded_by back to users.id int
    op.drop_constraint(op.f('fk_photos_uploaded_by_users'), 'photos', type_='foreignkey')
    op.alter_column('photos', 'uploaded_by',
                    existing_type=sa.UUID(),
                    type_=sa.Integer(),
                    postgresql_using='(uploaded_by::text)::integer',
                    nullable=True)
    # FK to users.id (int)
    op.create_foreign_key(op.f('fk_photos_uploaded_by_users'), 'photos', 'users', ['uploaded_by'], ['id'])
