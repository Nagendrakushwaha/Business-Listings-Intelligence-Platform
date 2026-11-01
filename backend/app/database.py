"""
Database connection, session management, and connection pooling for MySQL.
Reads credentials from environment variables safely.
Includes resilient fallback to local SQLite cache seeded from data/business_listings.csv
if MySQL credentials are not yet configured.
"""

import os
import csv
import logging
from pathlib import Path
from typing import Generator, Tuple, Optional
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from app.models import Base, ListingMaster

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

# Fallback SQLite DB path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CSV_PATH = BASE_DIR / "data" / "business_listings.csv"
FALLBACK_DB_PATH = BASE_DIR / "data" / "fallback_listings.db"
FALLBACK_URL = f"sqlite:///{FALLBACK_DB_PATH}"

# Primary MySQL Engine
try:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"connect_timeout": 3},
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.error(f"Failed to create MySQL engine: {e}")
    engine = None
    SessionLocal = None

# Fallback SQLite Engine
fallback_engine = create_engine(
    FALLBACK_URL,
    connect_args={"check_same_thread": False},
    echo=False
)
FallbackSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=fallback_engine)


def seed_fallback_db():
    """Populates fallback database from data/business_listings.csv if empty."""
    try:
        Base.metadata.create_all(bind=fallback_engine)
        session = FallbackSessionLocal()
        count = session.query(ListingMaster).count()
        if count == 0 and CSV_PATH.exists():
            logger.info(f"Seeding fallback database from {CSV_PATH}...")
            with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                items = []
                for row in reader:
                    lat = float(row["latitude"]) if row.get("latitude") and row["latitude"] != "None" else None
                    lon = float(row["longitude"]) if row.get("longitude") and row["longitude"] != "None" else None
                    phone = row.get("phone") if row.get("phone") and row["phone"] != "None" else None
                    items.append(ListingMaster(
                        business_name=row["business_name"],
                        category=row.get("category"),
                        city=row["city"],
                        address=row.get("address"),
                        phone=phone,
                        source=row.get("source", "OpenStreetMap"),
                        source_id=row.get("source_id"),
                        latitude=lat,
                        longitude=lon
                    ))
                if items:
                    session.add_all(items)
                    session.commit()
                    logger.info(f"Seeded {len(items)} listings into fallback database.")
        session.close()
    except Exception as e:
        logger.error(f"Error seeding fallback database: {e}")


def check_db_connection() -> Tuple[bool, Optional[str]]:
    """Checks whether connection to MySQL can be established."""
    if os.getenv("TESTING") == "1":
        return True, "SQLite (Test Mode)"
    if not engine:
        return False, "MySQL engine not initialized"
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION();")).fetchone()
            version = result[0] if result else "MySQL 8.0"
            return True, str(version)
    except Exception as e:
        return False, str(e)


def init_db() -> bool:
    """Safely creates the MySQL database & tables, and prepares fallback DB."""
    seed_fallback_db()

    if os.getenv("TESTING") == "1":
        return True

    try:
        # Connect to MySQL server to ensure DB exists
        temp_engine = create_engine(SERVER_URL, pool_pre_ping=True, connect_args={"connect_timeout": 3})
        with temp_engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"))
            conn.commit()
        temp_engine.dispose()

        # Create tables using the main engine
        if engine:
            Base.metadata.create_all(bind=engine)
            logger.info("MySQL database and tables initialized successfully.")
            return True
        return False
    except Exception as e:
        logger.warning(f"MySQL initialization deferred (using fallback): {e}")
        return False


def get_db() -> Generator[Session, None, None]:
    """Provides a database session: MySQL if connected, otherwise fallback session."""
    # First test if MySQL is reachable
    is_connected, _ = check_db_connection()
    if is_connected and SessionLocal:
        db = SessionLocal()
        try:
            yield db
        except OperationalError:
            # Fallback to local session on error
            db.close()
            fb_db = FallbackSessionLocal()
            try:
                yield fb_db
            finally:
                fb_db.close()
        finally:
            db.close()
    else:
        # Use fallback session
        fb_db = FallbackSessionLocal()
        try:
            yield fb_db
        finally:
            fb_db.close()
