import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# === Pastikan path project terdaftar ===
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# === Import Base dan settings dari project ===
from app.core.config import settings
from app.models import *  # agar metadata dari semua model ter-load
from app.core.database import Base  # jika kamu punya Base di file khusus

# Ini untuk konfigurasi logging
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# === Ganti URL Alembic dengan URL dari settings ===
config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URI)

# Ambil metadata dari semua model
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Jalankan migrasi dalam mode 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Jalankan migrasi dalam mode 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
