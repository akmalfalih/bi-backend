"""add index on TglTmb1 in TTransPemasaran

Revision ID: b69d8b6ed505
Revises: 09d535c60ddd
Create Date: 2025-10-20 13:39:13.513566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b69d8b6ed505'
down_revision: Union[str, None] = '09d535c60ddd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "idx_ttranspemasaran_tgltmb1",
        "TTransPemasaran",
        ["TglTmb1"]
    )

def downgrade() -> None:
    op.drop_index(
        "idx_ttranspemasaran_tgltmb1",
        table_name="TTransPemasaran"
    )