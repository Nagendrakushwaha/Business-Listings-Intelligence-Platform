"""
Service layer for Dashboard KPIs, aggregations, charts, and data quality metrics.
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import ListingMaster
from app.schemas import (
    DashboardSummaryResponse,
    CityWiseItem,
    CategoryWiseItem,
    SourceWiseItem,
    DataQualityReportResponse
)

logger = logging.getLogger("DashboardService")

REPORT_PATH = Path(__file__).resolve().parent.parent.parent.parent / "data" / "data_quality_report.json"


class DashboardService:
    @staticmethod
    def get_summary(db: Session) -> DashboardSummaryResponse:
        """
        Calculates high-level KPI metrics across all listings.
        """
        total_listings = db.query(func.count(ListingMaster.id)).scalar() or 0
        total_cities = db.query(func.count(func.distinct(ListingMaster.city))).scalar() or 0
        total_categories = db.query(func.count(func.distinct(ListingMaster.category))).scalar() or 0
        total_sources = db.query(func.count(func.distinct(ListingMaster.source))).scalar() or 0

        with_phone = db.query(func.count(ListingMaster.id)).filter(
            ListingMaster.phone.isnot(None),
            ListingMaster.phone != ""
        ).scalar() or 0

        without_phone = total_listings - with_phone
        coverage_pct = round((with_phone / total_listings * 100), 2) if total_listings > 0 else 0.0

        return DashboardSummaryResponse(
            total_listings=total_listings,
            total_cities=total_cities,
            total_categories=total_categories,
            total_sources=total_sources,
            with_phone=with_phone,
            without_phone=without_phone,
            phone_coverage_percentage=coverage_pct
        )

    @staticmethod
    def get_city_wise(db: Session) -> List[CityWiseItem]:
        """
        Calculates listing counts and percentage distribution by city.
        """
        total = db.query(func.count(ListingMaster.id)).scalar() or 0
        if total == 0:
            return []

        results = db.query(
            ListingMaster.city,
            func.count(ListingMaster.id).label("count")
        ).group_by(ListingMaster.city).order_by(func.count(ListingMaster.id).desc()).all()

        return [
            CityWiseItem(
                city=city,
                count=count,
                percentage=round((count / total) * 100, 2)
            )
            for city, count in results
        ]

    @staticmethod
    def get_category_wise(db: Session) -> List[CategoryWiseItem]:
        """
        Calculates listing counts and percentage distribution by category.
        """
        total = db.query(func.count(ListingMaster.id)).scalar() or 0
        if total == 0:
            return []

        results = db.query(
            ListingMaster.category,
            func.count(ListingMaster.id).label("count")
        ).group_by(ListingMaster.category).order_by(func.count(ListingMaster.id).desc()).all()

        return [
            CategoryWiseItem(
                category=cat or "Uncategorized",
                count=count,
                percentage=round((count / total) * 100, 2)
            )
            for cat, count in results
        ]

    @staticmethod
    def get_source_wise(db: Session) -> List[SourceWiseItem]:
        """
        Calculates listing counts and percentage distribution by data source.
        """
        total = db.query(func.count(ListingMaster.id)).scalar() or 0
        if total == 0:
            return []

        results = db.query(
            ListingMaster.source,
            func.count(ListingMaster.id).label("count")
        ).group_by(ListingMaster.source).order_by(func.count(ListingMaster.id).desc()).all()

        return [
            SourceWiseItem(
                source=source,
                count=count,
                percentage=round((count / total) * 100, 2)
            )
            for source, count in results
        ]

    @staticmethod
    def get_data_quality(db: Session) -> DataQualityReportResponse:
        """
        Returns the formal data quality report, grounded in scraped report or live DB.
        """
        if REPORT_PATH.exists():
            try:
                with open(REPORT_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return DataQualityReportResponse(**data)
            except Exception as e:
                logger.error(f"Error loading report file: {e}")

        # Fallback to computing from live DB
        summary = DashboardService.get_summary(db)
        city_dist = {item.city: item.count for item in DashboardService.get_city_wise(db)}
        cat_dist = {item.category: item.count for item in DashboardService.get_category_wise(db)}
        src_dist = {item.source: item.count for item in DashboardService.get_source_wise(db)}

        return DataQualityReportResponse(
            total_raw_records=summary.total_listings,
            total_cleaned_records=summary.total_listings,
            duplicates_removed=0,
            duplicate_source_ids=0,
            duplicate_business_name_city=0,
            empty_business_names_removed=0,
            invalid_coordinates_detected=0,
            missing_phone_numbers=summary.without_phone,
            present_phone_numbers=summary.with_phone,
            missing_addresses=0,
            phone_coverage_percentage=summary.phone_coverage_percentage,
            records_per_city=city_dist,
            records_per_category=cat_dist,
            records_per_source=src_dist,
            pipeline_status="LIVE_DATABASE"
        )

