"""add jwt auth user fields

Revision ID: 202605270001
Revises: 7c62492eb528
Create Date: 2026-05-27 00:00:01.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "202605270001"
down_revision: Union[str, None] = "7c62492eb528"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("name", sa.String(length=255), nullable=True))
    op.add_column("users", sa.Column("hashed_password", sa.String(length=255), nullable=True))
    op.add_column(
        "users",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )

    op.execute("UPDATE users SET name = full_name WHERE name IS NULL")
    op.execute("UPDATE users SET hashed_password = password_hash WHERE hashed_password IS NULL")

    op.alter_column("users", "name", nullable=False)
    op.alter_column("users", "hashed_password", nullable=False)

    op.execute("ALTER TABLE users DROP CONSTRAINT IF EXISTS users_role_check")
    op.create_check_constraint(
        "users_role_check",
        "users",
        "role IN ('student', 'admin', 'teacher')",
    )

    op.drop_column("users", "full_name")
    op.drop_column("users", "password_hash")


def downgrade() -> None:
    op.add_column("users", sa.Column("full_name", sa.Text(), nullable=True))
    op.add_column("users", sa.Column("password_hash", sa.Text(), nullable=True))

    op.execute("UPDATE users SET full_name = name WHERE full_name IS NULL")
    op.execute("UPDATE users SET password_hash = hashed_password WHERE password_hash IS NULL")

    op.alter_column("users", "full_name", nullable=False)
    op.alter_column("users", "password_hash", nullable=False)

    op.execute("ALTER TABLE users DROP CONSTRAINT IF EXISTS users_role_check")
    op.create_check_constraint(
        "users_role_check",
        "users",
        "role IN ('student', 'admin')",
    )

    op.drop_column("users", "is_active")
    op.drop_column("users", "hashed_password")
    op.drop_column("users", "name")