"""add review foreign keys

Revision ID: 3212546ce0e2
Revises: 578424094842
Create Date: 2025-11-30 23:50:04.893578

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3212546ce0e2'
down_revision: Union[str, Sequence[str], None] = '578424094842'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_foreign_key(
        "fk_product_reviews_product_id",
        "product_reviews",
        "products",
        ["product_id"],
        ["id"],
        ondelete="CASCADE"
    )
    op.create_foreign_key(
        "fk_product_reviews_user_id",
        "product_reviews",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE"
    )

def downgrade():
    op.drop_constraint(
        "fk_product_reviews_product_id",
        "product_reviews",
        type_="foreignkey"
    )
    op.drop_constraint(
        "fk_product_reviews_user_id",
        "product_reviews",
        type_="foreignkey"
    )
