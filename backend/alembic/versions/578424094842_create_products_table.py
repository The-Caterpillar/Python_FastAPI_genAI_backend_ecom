"""create_products_table

Revision ID: 578424094842
Revises: 138cb3e34008
Create Date: 2025-11-30 23:05:24.163216

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "578424094842"
down_revision = "138cb3e34008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False, index=True),
        sa.Column("short_description", sa.String(), nullable=True),
        sa.Column("long_description", sa.Text(), nullable=True),
        sa.Column("price", sa.Numeric(10, 2), nullable=False, server_default=sa.text("'0.00'")),
        sa.Column("stock", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column(
            "currency",
            sa.Enum("INR", "USD", "EUR", name="currency_enum"),
            nullable=False,
            server_default=sa.text("'INR'"),
        ),
        sa.Column("in_stock", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_products_name"), table_name="products")
    op.drop_table("products")
    # drop enum type (Postgres)
    op.execute("DROP TYPE IF EXISTS currency_enum;")
