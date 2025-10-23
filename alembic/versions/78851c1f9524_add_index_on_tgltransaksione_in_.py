"""add index on TglTransaksiOne in TTbsDalam

Revision ID: 78851c1f9524
Revises: 3a2b6f89cd12
Create Date: 2025-10-17 15:47:37.058640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78851c1f9524'
down_revision: Union[str, None] = '3a2b6f89cd12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Membuat index baru di kolom TglTransaksiOne
    op.create_index('idx_tgltransaksione', 'TTbsDalam', ['TglTransaksiOne'], unique=False)


def downgrade() -> None:
    # Menghapus index jika rollback
    op.drop_index('idx_tgltransaksione', table_name='TTbsDalam')