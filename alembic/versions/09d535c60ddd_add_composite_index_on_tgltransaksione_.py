"""add composite index on TglTransaksiOne and NamaKebun in TTbsDalam

Revision ID: 09d535c60ddd
Revises: 78851c1f9524
Create Date: 2025-10-17 15:54:08.022039

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09d535c60ddd'
down_revision: Union[str, None] = '78851c1f9524'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create composite index for faster filtering by date and origin (NamaKebun)
    op.create_index(
        'idx_tgltransaksi_namakebun',
        'TTbsDalam',
        ['TglTransaksiOne', 'NamaKebun'],
        unique=False
    )


def downgrade() -> None:
    # Drop the composite index if rollback is needed
    op.drop_index('idx_tgltransaksi_namakebun', table_name='TTbsDalam')