"""
CSV Export Utility for Business Listings Intelligence Platform.
Exports listings to CSV with full UTF-8 encoding and Excel compatibility.

Usage:
    python -m scraper.export_csv
    python backend/scraper/export_csv.py --city Bhopal --output data/bhopal_listings.csv
"""

import os
import sys
import argparse
import logging
import pandas as pd

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from .config import CLEAN_DATA_PATH, DATA_DIR
except ImportError:
    from config import CLEAN_DATA_PATH, DATA_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("CSVExporter")


def export_listings(
    source_csv=CLEAN_DATA_PATH,
    output_path=None,
    city=None,
    category=None,
    source=None
):
    """Exports listings with optional filtering to a clean, Excel-compatible CSV file."""
    if not os.path.exists(source_csv):
        logger.error(f"Source file {source_csv} not found.")
        return False

    df = pd.read_csv(source_csv, encoding="utf-8")
    initial_count = len(df)

    if city:
        df = df[df["city"].str.lower() == city.lower()]
    if category:
        df = df[df["category"].str.lower() == category.lower()]
    if source:
        df = df[df["source"].str.lower() == source.lower()]

    out_file = output_path or source_csv
    df.to_csv(out_file, index=False, encoding="utf-8-sig")

    logger.info(f"Exported {len(df)} of {initial_count} records to {out_file} (UTF-8 with BOM for Excel)")
    return True


def main():
    parser = argparse.ArgumentParser(description="Export business listings to CSV.")
    parser.add_argument("--source", default=str(CLEAN_DATA_PATH), help="Source CSV path.")
    parser.add_argument("--output", default=None, help="Output CSV path.")
    parser.add_argument("--city", default=None, help="Filter by city.")
    parser.add_argument("--category", default=None, help="Filter by category.")
    args = parser.parse_args()

    export_listings(
        source_csv=args.source,
        output_path=args.output,
        city=args.city,
        category=args.category
    )


if __name__ == "__main__":
    main()

