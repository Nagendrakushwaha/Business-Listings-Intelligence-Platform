"""
Dashboard analytics routes for summary KPIs, city/category/source distributions, and data quality metrics.
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas import (
    DashboardSummaryResponse,
    CityWiseItem,
    CategoryWiseItem,
    SourceWiseItem,
    DataQualityReportResponse
)
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Returns top-level KPI metrics for total businesses, cities, categories, sources, and phone coverage."""
    return DashboardService.get_summary(db)


@router.get("/city-wise", response_model=List[CityWiseItem])
def get_city_wise_analytics(db: Session = Depends(get_db)):
    """Returns business listings count and percentage distribution by city."""
    return DashboardService.get_city_wise(db)


@router.get("/category-wise", response_model=List[CategoryWiseItem])
def get_category_wise_analytics(db: Session = Depends(get_db)):
    """Returns business listings count and percentage distribution by category."""
    return DashboardService.get_category_wise(db)


@router.get("/source-wise", response_model=List[SourceWiseItem])
def get_source_wise_analytics(db: Session = Depends(get_db)):
    """Returns business listings count and percentage distribution by data source."""
    return DashboardService.get_source_wise(db)


@router.get("/data-quality", response_model=DataQualityReportResponse)
def get_data_quality_report(db: Session = Depends(get_db)):
    """Returns comprehensive data quality metrics including duplicates removed, missing fields, and coverage."""
    return DashboardService.get_data_quality(db)

