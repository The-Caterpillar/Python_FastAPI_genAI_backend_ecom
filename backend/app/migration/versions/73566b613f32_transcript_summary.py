"""transcript_summary

Revision ID: 73566b613f32
Revises: 
Create Date: 2024-02-09 16:19:29.267182

"""

from typing import Sequence, Union
from sqlalchemy import INTEGER, VARCHAR, NVARCHAR, Column, TIMESTAMP, func, JSON, String
from alembic import op

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "73566b613f32"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
