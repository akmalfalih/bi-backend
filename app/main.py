import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI
from urllib.parse import urlparse
from app.core.config import settings
from app.core.database import Base, engine
from app.routers import auth


# === Setup Logging ===
log_formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    "%Y-%m-%d %H:%M:%S",
)

log_file_path = f"{settings.LOG_DIR}/{settings.LOG_FILE}"

# Log ke file (rotating 5 MB)
file_handler = RotatingFileHandler(
    log_file_path, maxBytes=5 * 1024 * 1024, backupCount=3
)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

# Log ke console
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)

# Setup logger utama
logger = logging.getLogger("APN-Riau")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# === FastAPI App ===
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)


@app.on_event("startup")
def startup_event():
    """Log informasi konfigurasi saat server mulai"""
    parsed_db = urlparse(settings.DATABASE_URL)
    db_info = f"{parsed_db.scheme}://{parsed_db.hostname or 'localhost'}/{parsed_db.path.lstrip('/')}"

    logger.info("=== Application Startup ===")
    logger.info(f"App Name     : {settings.APP_NAME}")
    logger.info(f"Version      : {settings.APP_VERSION}")
    logger.info(f"Database URL : {db_info}")
    logger.info(f"Debug Mode   : {settings.DEBUG}")
    logger.info("==============================")

    # Buat tabel jika belum ada
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ready.")


@app.get("/")
def root():
    logger.info("Root endpoint accessed.")
    return {"message": f"{settings.APP_NAME} is running"}


# Tambahkan router auth
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
