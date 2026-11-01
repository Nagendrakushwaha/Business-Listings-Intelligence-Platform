"""
Database Seeder and SQL Dump Generator for Business Listings Intelligence Platform.
Imports data/business_listings.csv into MySQL and generates database/business_listings.sql.

Usage:
    python database/seed_data.py
    python database/seed_data.py --dump-only
"""

import os
import sys
import csv
import argparse
import logging
from pathlib import Path

# Add backend directory to path
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from dotenv import load_dotenv
load_dotenv(BACKEND_DIR / ".env")

from app.database import engine, init_db, check_db_connection, DB_NAME
from app.models import ListingMaster
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DatabaseSeeder")

CSV_PATH = BASE_DIR / "data" / "business_listings.csv"
SQL_DUMP_PATH = BASE_DIR / "database" / "business_listings.sql"


def generate_sql_dump(csv_path: Path = CSV_PATH, dump_path: Path = SQL_DUMP_PATH):
    """Generates an independent, complete MySQL database dump file (.sql)."""
    if not csv_path.exists():
        logger.error(f"Cannot generate SQL dump: {csv_path} does not exist.")
        return False

    logger.info(f"Generating MySQL dump at {dump_path}...")
    dump_lines = [
        "-- ============================================================",
        "-- Business Listings Intelligence Platform",
        "-- MySQL Database Dump",
        "-- Target Database: business_listings_db",
        "-- Target Table: listing_master",
        "-- ============================================================",
        "",
        "CREATE DATABASE IF NOT EXISTS `business_listings_db`",
        "    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
        "",
        "USE `business_listings_db`;",
        "",
        "DROP TABLE IF EXISTS `listing_master`;",
        "",
        "CREATE TABLE `listing_master` (",
        "    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,",
        "    `business_name` VARCHAR(255) NOT NULL,",
        "    `category` VARCHAR(100),",
        "    `city` VARCHAR(100) NOT NULL,",
        "    `address` TEXT,",
        "    `phone` VARCHAR(30),",
        "    `source` VARCHAR(100) NOT NULL,",
        "    `source_id` VARCHAR(150),",
        "    `latitude` DECIMAL(10,7),",
        "    `longitude` DECIMAL(10,7),",
        "    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,",
        "",
        "    UNIQUE KEY `unique_source_listing` (`source`, `source_id`),",
        "    INDEX `idx_city` (`city`),",
        "    INDEX `idx_category` (`category`),",
        "    INDEX `idx_source` (`source`)",
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;",
        "",
        "-- Dumping data for table `listing_master`",
        "LOCK TABLES `listing_master` WRITE;",
        ""
    ]

    insert_rows = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("business_name", "").replace("'", "''")
            cat = row.get("category", "").replace("'", "''")
            city = row.get("city", "").replace("'", "''")
            addr = row.get("address", "").replace("'", "''")
            phone = row.get("phone", "")
            source = row.get("source", "OpenStreetMap").replace("'", "''")
            sid = row.get("source_id", "").replace("'", "''")
            lat = row.get("latitude")
            lon = row.get("longitude")

            phone_val = f"'{phone}'" if phone and phone != "None" else "NULL"
            cat_val = f"'{cat}'" if cat else "NULL"
            addr_val = f"'{addr}'" if addr else "NULL"
            lat_val = lat if lat and lat != "None" else "NULL"
            lon_val = lon if lon and lon != "None" else "NULL"

            insert_rows.append(
                f"('{name}', {cat_val}, '{city}', {addr_val}, {phone_val}, '{source}', '{sid}', {lat_val}, {lon_val})"
            )

    # Write inserts in chunks of 50 rows
    chunk_size = 50
    for i in range(0, len(insert_rows), chunk_size):
        chunk = insert_rows[i:i + chunk_size]
        sql_stmt = (
            "INSERT INTO `listing_master` "
            "(`business_name`, `category`, `city`, `address`, `phone`, `source`, `source_id`, `latitude`, `longitude`) VALUES\n"
            + ",\n".join(chunk) + ";\n"
        )
        dump_lines.append(sql_stmt)

    dump_lines.extend([
        "UNLOCK TABLES;",
        "",
        "-- Dump completed successfully."
    ])

    with open(dump_path, "w", encoding="utf-8") as f:
        f.write("\n".join(dump_lines))

    logger.info(f"SQL dump successfully generated with {len(insert_rows)} records at {dump_path}")
    return True


def seed_mysql_database():
    """Connects to live MySQL database and seeds it with data from CSV."""
    is_connected, msg = check_db_connection()
    if not is_connected:
        logger.warning(f"Could not connect to MySQL: {msg}")
        logger.info("Make sure MySQL is running and DB credentials in backend/.env are configured.")
        return False

    logger.info(f"Connected to MySQL ({msg}). Initializing schema...")
    init_db()

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        existing_count = session.query(ListingMaster).count()
        logger.info(f"Existing listings in MySQL: {existing_count}")

        with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            new_objects = []
            seen_ids = set()

            for row in reader:
                sid = row.get("source_id")
                source = row.get("source", "OpenStreetMap")
                if sid in seen_ids:
                    continue
                seen_ids.add(sid)

                # Check if exists
                exists = session.query(ListingMaster).filter_by(source=source, source_id=sid).first()
                if exists:
                    continue

                lat = float(row["latitude"]) if row.get("latitude") and row["latitude"] != "None" else None
                lon = float(row["longitude"]) if row.get("longitude") and row["longitude"] != "None" else None
                phone = row.get("phone") if row.get("phone") and row["phone"] != "None" else None

                obj = ListingMaster(
                    business_name=row["business_name"],
                    category=row.get("category"),
                    city=row["city"],
                    address=row.get("address"),
                    phone=phone,
                    source=source,
                    source_id=sid,
                    latitude=lat,
                    longitude=lon
                )
                new_objects.append(obj)

        if new_objects:
            logger.info(f"Seeding {len(new_objects)} new records into MySQL...")
            session.bulk_save_objects(new_objects)
            session.commit()
            logger.info("Seeding completed successfully!")
        else:
            logger.info("Database is already up to date with all records.")

        total = session.query(ListingMaster).count()
        logger.info(f"Total listings in database now: {total}")
        return True
    except Exception as e:
        session.rollback()
        logger.error(f"Error seeding database: {e}")
        return False
    finally:
        session.close()


def main():
    parser = argparse.ArgumentParser(description="Database Seeder & SQL Dump Tool.")
    parser.add_argument("--dump-only", action="store_true", help="Generate SQL dump without connecting to MySQL.")
    args = parser.parse_args()

    # Always generate SQL dump
    generate_sql_dump()

    if not args.dump_only:
        seed_mysql_database()


if __name__ == "__main__":
    main()

