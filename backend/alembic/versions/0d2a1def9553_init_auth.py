"""init auth

Revision ID: 0d2a1def9553
Revises: a3c6ff30da96
Create Date: 2025-11-29 23:31:53.126910
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '0d2a1def9553'
down_revision: Union[str, Sequence[str], None] = 'a3c6ff30da96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # --- Remove old admin_users table ---
    op.drop_index(op.f('ix_admin_users_email'), table_name='admin_users')
    op.drop_index(op.f('ix_admin_users_id'), table_name='admin_users')
    op.drop_table('admin_users')

    # --- Create ENUM before using it ---
    op.execute("CREATE TYPE user_role_enum AS ENUM ('customer','admin')")

    # --- Add role column to users ---
    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.Enum('customer', 'admin', name='user_role_enum'),
            server_default='customer',
            nullable=False
        )
    )

    # --- Ensure password_hash is NOT NULL ---
    op.alter_column(
        'users',
        'password_hash',
        existing_type=sa.VARCHAR(),
        nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    # --- Revert password_hash nullable ---
    op.alter_column(
        'users',
        'password_hash',
        existing_type=sa.VARCHAR(),
        nullable=True
    )

    # --- Remove role column ---
    op.drop_column('users', 'role')

    # --- Drop enum type ---
    op.execute("DROP TYPE user_role_enum")

    # --- Recreate admin_users table ---
    op.create_table(
        'admin_users',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('email', sa.VARCHAR(), nullable=False),
        sa.Column('password_hash', sa.VARCHAR(), nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True),
                  server_default=sa.text('now()'),
                  nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('admin_users_pkey'))
    )
    op.create_index(op.f('ix_admin_users_id'), 'admin_users', ['id'], unique=False)
    op.create_index(op.f('ix_admin_users_email'), 'admin_users', ['email'], unique=True)
