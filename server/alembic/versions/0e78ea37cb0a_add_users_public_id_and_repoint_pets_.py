"""add_users_public_id_and_repoint_pets_owner_fk

Revision ID: 0e78ea37cb0a
Revises: 0a393ca192dd
Create Date: 2025-09-25 17:35:28.992569

"""
from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision = '0e78ea37cb0a'
down_revision = '0a393ca192dd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1) Add users.public_id (UUID) with temp nullable=True to backfill
    op.add_column('users', sa.Column('public_id', sa.UUID(), nullable=True))
    op.create_index('ix_users_public_id', 'users', ['public_id'], unique=True)

    # Backfill existing users with generated UUIDs
    connection = op.get_bind()
    users = connection.execute(sa.text("SELECT id FROM users WHERE public_id IS NULL")).fetchall()
    for row in users:
        connection.execute(
            sa.text("UPDATE users SET public_id = :pid WHERE id = :id"),
            { 'pid': str(uuid.uuid4()), 'id': row.id }
        )

    # Make column non-nullable after backfill
    op.alter_column('users', 'public_id', nullable=False)

    # 2) Repoint pets.owner_id FK from owners.id to users.public_id
    # Drop existing FK
    op.drop_constraint(op.f('fk_pets_owner_id_owners'), 'pets', type_='foreignkey')
    # Create new FK to users.public_id
    op.create_foreign_key(op.f('fk_pets_owner_id_users'), 'pets', 'users', ['owner_id'], ['public_id'])


def downgrade() -> None:
    # Revert pets.owner_id FK back to owners.id
    op.drop_constraint(op.f('fk_pets_owner_id_users'), 'pets', type_='foreignkey')
    op.create_foreign_key(op.f('fk_pets_owner_id_owners'), 'pets', 'owners', ['owner_id'], ['id'])

    # Drop users.public_id
    op.drop_index('ix_users_public_id', table_name='users')
    op.drop_column('users', 'public_id')
