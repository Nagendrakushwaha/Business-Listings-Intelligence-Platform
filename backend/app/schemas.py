"""
Pydantic Schemas for Request/Response validation in FastAPI.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class ListingBase(BaseModel):
    business_name: str = Field(..., min_length=1, max_length=255, description="Official business name")
    category: Optional[str] = Field(None, max_length=100, description="Standardized business category")
    city: str = Field(..., min_length=1, max_length=100, description="City location")
    address: Optional[str] = Field(None, description="Street address or locality details")
    phone: Optional[str] = Field(None, max_length=30, description="Contact phone number")
    source: str = Field(..., max_length=100, description="Data source identifier")
    source_id: Optional[str] = Field(None, max_length=150, description="Origin unique ID")
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0, description="Geographic latitude")
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0, description="Geographic longitude")


class ListingCreate(ListingBase):
    pass


class ListingResponse(ListingBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class BulkListingCreate(BaseModel):
    listings: List[ListingCreate] = Field(..., description="Array of business listing objects to insert")


class BulkInsertResponse(BaseModel):
    inserted: int
    skipped: int
    failed: int
    message: str
    errors: Optional[List[str]] = None


class PaginatedListingsResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[ListingResponse]


class DashboardSummaryResponse(BaseModel):
    total_listings: int
    total_cities: int
    total_categories: int
    total_sources: int
    with_phone: int
    without_phone: int
    phone_coverage_percentage: float


class CityWiseItem(BaseModel):
    city: str
    count: int
    percentage: float


class CategoryWiseItem(BaseModel):
    category: str
    count: int
    percentage: float


class SourceWiseItem(BaseModel):
    source: str
    count: int
    percentage: float


class DataQualityReportResponse(BaseModel):
    total_raw_records: int
    total_cleaned_records: int
    duplicates_removed: int
    duplicate_source_ids: int
    duplicate_business_name_city: int
    empty_business_names_removed: int
    invalid_coordinates_detected: int
    missing_phone_numbers: int
    present_phone_numbers: int
    missing_addresses: int
    phone_coverage_percentage: float
    records_per_city: Dict[str, int]
    records_per_category: Dict[str, int]
    records_per_source: Dict[str, int]
    pipeline_status: str


class HealthResponse(BaseModel):
    status: str
    database_connected: bool
    database_version: Optional[str] = None
    timestamp: datetime

