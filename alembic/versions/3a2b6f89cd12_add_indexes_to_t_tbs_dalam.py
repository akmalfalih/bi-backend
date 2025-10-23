"""add indexes to TTbsDalam for optimization

Revision ID: 3a2b6f89cd12
Revises: 60f9d711d993
Create Date: 2025-10-14 22:30:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a2b6f89cd12'
down_revision = '60f9d711d993'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Tambahkan index untuk optimasi filter dan group-by
    op.create_index('idx_tgltransaksi_tbsdalam', 'TTbsDalam', ['TglTransaksiOne'])
    op.create_index('idx_namakebun_tbsdalam', 'TTbsDalam', ['NamaKebun'])


def downgrade() -> None:
    # Hapus index jika perlu rollback
    op.drop_index('idx_tgltransaksi_tbsdalam', table_name='TTbsDalam')
    op.drop_index('idx_namakebun_tbsdalam', table_name='TTbsDalam')
