"""
Database connection, session management, and connection pooling for MySQL.
Reads credentials from environment variables safely.
"""

import os
import logging
from typing import Generator, Tuple, Optional
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from app.models import Base

load_dotenv()

logger = logging.getLogger("Database")

# Configuration via environment variables
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "business_listings_db")

# Construct URL (password safely URL-encoded)
encoded_password = quote_plus(DB_PASSWORD) if DB_PASSWORD else ""
auth_part = f"{DB_USER}:{encoded_password}@" if encoded_password else f"{DB_USER}@"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"mysql+pymysql://{auth_part}{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)

# Root server URL without specific database (used for auto-creation)
SERVER_URL = f"mysql+pymysql://{auth_part}{DB_HOST}:{DB_PORT}/?charset=utf8mb4"

# Connection Pool Configuration
try:
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.error(f"Failed to create SQLAlchemy engine: {e}")
    engine = None
    SessionLocal = None


def get_db() -> Generator[Session, None, None]:
    """Dependency that provides a database session per request."""
    if not SessionLocal:
        raise RuntimeError("Database engine not initialized. Check your database configuration.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> Tuple[bool, Optional[str]]:
    """Checks whether connection to MySQL can be established."""
    if os.getenv("TESTING") == "1":
        return True, "SQLite (Test Mode)"
    if not engine:
        return False, "Database engine is not initialized"
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION();")).fetchone()
            version = result[0] if result else "MySQL"
            return True, str(version)
    except Exception as e:
        return False, str(e)


def init_db() -> bool:
    """Safely creates the database if it doesn't exist, and creates all tables."""
    if os.getenv("TESTING") == "1":
        return True
    try:
        # First connect to MySQL server to ensure DB exists
        temp_engine = create_engine(SERVER_URL, pool_pre_ping=True)
        with temp_engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"))
            conn.commit()
        temp_engine.dispose()

        # Then create tables using the main engine
        if engine:
            Base.metadata.create_all(bind=engine)
            logger.info("Database and tables initialized successfully.")
            return True
        return False
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        return False
