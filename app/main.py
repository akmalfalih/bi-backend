import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request, Depends
from urllib.parse import urlparse
from app.core.config import settings
from app.core.database import Base, engine
from app.routers import auth, dashboard
import time
from jose import JWTError
from app.core.security import decode_access_token
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


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

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event menggantikan on_event('startup')"""
    # === Startup ===
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

    # yield = FastAPI “running” phase
    yield

    # === Shutdown ===
    logger.info("=== Application Shutdown ===")


# === FastAPI App ===
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Izinkan akses dari frontend Vite
origins = [
    "http://localhost:5173",  # frontend dev
    "http://127.0.0.1:5173",  # alternatif dev
    "http://localhost:3000",  # frontend dev
    "http://127.0.0.1:3000",  # alternatif dev
    "http://103.49.239.26/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],      # izinkan semua method (GET, POST, dll)
    allow_headers=["*"],      # izinkan semua header
)

# === Middleware: HTTP Request Logging + Username ===
@app.middleware("http")
async def log_http_requests(request: Request, call_next):
    """
    Middleware untuk mencatat semua request HTTP,
    termasuk user (diambil dari JWT jika ada).
    """
    start_time = time.time()
    username = "anonymous"  # default jika belum login

    # Coba ambil username dari Authorization header
    try:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            payload = decode_access_token(token)
            username = payload.get("sub", "unknown") if payload else "anonymous"
    except JWTError:
        username = "invalid_token"

    # Jalankan endpoint target
    try:
        response = await call_next(request)
    except Exception as e:
        logger.exception(f"[{username}] {request.method} {request.url.path} raised error: {e}")
        raise

    # Hitung waktu proses
    process_time = (time.time() - start_time) * 1000  # ms
    client_host = request.client.host if request.client else "unknown"

    logger.info(
        f"[{username}] {request.method} {request.url.path} "
        f"- {response.status_code} ({process_time:.2f} ms) from {client_host}"
    )

    return response


@app.get("/")
def root():
    logger.info("Root endpoint accessed.")
    return {"message": f"{settings.APP_NAME} is running"}


# Tambahkan router auth
app.include_router(auth.router, tags=["Authentication"])
app.include_router(dashboard.router, tags=["Dashboard"])
