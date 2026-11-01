"""
Listing management routes: bulk insert, search, filter, pagination, and CSV export.
"""

from typing import Optional, List, Union
from fastapi import APIRouter, Depends, Query, Response, HTTPException, Body
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas import (
    ListingCreate,
    BulkListingCreate,
    BulkInsertResponse,
    PaginatedListingsResponse
)
from app.services.listing_service import ListingService

router = APIRouter(prefix="/listings", tags=["Listings"])


@router.post("/bulk", response_model=BulkInsertResponse)
def bulk_insert_listings(
    payload: Union[BulkListingCreate, List[ListingCreate]] = Body(...),
    db: Session = Depends(get_db)
):
    """
    Bulk insert validated listings into MySQL.
    Accepts either a JSON array `[...]` or an object `{"listings": [...]}`.
    Detects duplicates and returns inserted, skipped, and failed counts.
    """
    if isinstance(payload, BulkListingCreate):
        items = payload.listings
    elif isinstance(payload, list):
        items = payload
    else:
        raise HTTPException(status_code=400, detail="Invalid payload format")

    if not items:
        return BulkInsertResponse(
            inserted=0,
            skipped=0,
            failed=0,
            message="No listings provided in request."
        )

    return ListingService.bulk_insert(db, items)


@router.get("", response_model=PaginatedListingsResponse)
def get_listings(
    search: Optional[str] = Query(None, description="Search by business name"),
    city: Optional[str] = Query(None, description="Filter by city name"),
    category: Optional[str] = Query(None, description="Filter by business category"),
    source: Optional[str] = Query(None, description="Filter by data source"),
    sort_by: str = Query("id", description="Column to sort by (id, business_name, city, category, created_at)"),
    sort_desc: bool = Query(False, description="Sort descending if true"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Fetch paginated, searchable, and filtered business listings.
    """
    valid_sort_cols = ["id", "business_name", "category", "city", "source", "created_at"]
    if sort_by not in valid_sort_cols:
        sort_by = "id"

    return ListingService.get_paginated(
        db=db,
        search=search,
        city=city,
        category=category,
        source=source,
        sort_by=sort_by,
        sort_desc=sort_desc,
        page=page,
        page_size=page_size
    )


@router.get("/export")
def export_listings_csv(
    search: Optional[str] = Query(None, description="Search filter for export"),
    city: Optional[str] = Query(None, description="City filter for export"),
    category: Optional[str] = Query(None, description="Category filter for export"),
    source: Optional[str] = Query(None, description="Source filter for export"),
    db: Session = Depends(get_db)
):
    """
    Exports filtered or complete business listings to an Excel-compatible CSV file.
    """
    csv_content = ListingService.export_csv(
        db=db,
        search=search,
        city=city,
        category=category,
        source=source
    )

    # Prepend UTF-8 BOM (\ufeff) for automatic UTF-8 recognition in Microsoft Excel
    csv_with_bom = "\ufeff" + csv_content

    filename = "business_listings_export.csv"
    if city:
        filename = f"business_listings_{city.lower()}.csv"

    return Response(
        content=csv_with_bom,
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )

