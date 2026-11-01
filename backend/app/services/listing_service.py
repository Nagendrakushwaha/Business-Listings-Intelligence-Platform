"""
Service layer for Business Listings management, querying, bulk insert, and export.
"""

import io
import csv
import logging
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc, func
from app.models import ListingMaster
from app.schemas import (
    ListingCreate,
    ListingResponse,
    BulkInsertResponse,
    PaginatedListingsResponse
)
from app.utils.validators import sanitize_search_query

logger = logging.getLogger("ListingService")


class ListingService:
    @staticmethod
    def bulk_insert(db: Session, items: List[ListingCreate]) -> BulkInsertResponse:
        """
        Inserts listings in bulk with transaction management and duplicate skipping.
        Returns counts for inserted, skipped (duplicate), and failed.
        """
        inserted_count = 0
        skipped_count = 0
        failed_count = 0
        error_messages = []

        # Find existing (source, source_id) combinations to prevent DB unique key violation
        incoming_source_ids = [item.source_id for item in items if item.source_id]
        existing_keys = set()
        if incoming_source_ids:
            # Query in chunks if large
            chunk_size = 500
            for i in range(0, len(incoming_source_ids), chunk_size):
                chunk = incoming_source_ids[i:i + chunk_size]
                existing = db.query(ListingMaster.source, ListingMaster.source_id).filter(
                    ListingMaster.source_id.in_(chunk)
                ).all()
                for s, sid in existing:
                    existing_keys.add((s, sid))

        seen_in_batch = set()
        new_records = []

        for item in items:
            key = (item.source, item.source_id) if item.source_id else None
            
            # Check if duplicate in DB or duplicate within incoming batch
            if key and (key in existing_keys or key in seen_in_batch):
                skipped_count += 1
                continue

            if key:
                seen_in_batch.add(key)

            try:
                record = ListingMaster(
                    business_name=item.business_name.strip(),
                    category=item.category.strip() if item.category else None,
                    city=item.city.strip(),
                    address=item.address.strip() if item.address else None,
                    phone=item.phone.strip() if item.phone else None,
                    source=item.source.strip(),
                    source_id=item.source_id.strip() if item.source_id else None,
                    latitude=item.latitude,
                    longitude=item.longitude
                )
                new_records.append(record)
            except Exception as e:
                failed_count += 1
                error_messages.append(f"Validation error for '{item.business_name}': {str(e)}")

        if new_records:
            try:
                db.add_all(new_records)
                db.commit()
                inserted_count = len(new_records)
            except Exception as e:
                db.rollback()
                logger.error(f"Bulk commit error: {e}")
                # Fallback to row-by-row insertion to salvage valid rows
                for r in new_records:
                    try:
                        db.add(r)
                        db.commit()
                        inserted_count += 1
                    except Exception as row_err:
                        db.rollback()
                        failed_count += 1
                        error_messages.append(f"Row insert failed for '{r.business_name}': {row_err}")

        return BulkInsertResponse(
            inserted=inserted_count,
            skipped=skipped_count,
            failed=failed_count,
            message=f"Processed {len(items)} listings: {inserted_count} inserted, {skipped_count} skipped, {failed_count} failed.",
            errors=error_messages[:10] if error_messages else None
        )

    @staticmethod
    def get_paginated(
        db: Session,
        search: Optional[str] = None,
        city: Optional[str] = None,
        category: Optional[str] = None,
        source: Optional[str] = None,
        sort_by: str = "id",
        sort_desc: bool = False,
        page: int = 1,
        page_size: int = 20
    ) -> PaginatedListingsResponse:
        """
        Retrieves paginated, filtered, and sorted business listings.
        """
        query = db.query(ListingMaster)

        # Filters
        if search:
            sanitized = sanitize_search_query(search)
            if sanitized:
                query = query.filter(ListingMaster.business_name.ilike(f"%{sanitized}%"))

        if city and city.strip():
            query = query.filter(func.lower(ListingMaster.city) == city.strip().lower())

        if category and category.strip():
            query = query.filter(func.lower(ListingMaster.category) == category.strip().lower())

        if source and source.strip():
            query = query.filter(func.lower(ListingMaster.source) == source.strip().lower())

        total = query.count()

        # Sorting
        sort_column = getattr(ListingMaster, sort_by, ListingMaster.id)
        if sort_desc:
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        # Pagination
        page = max(1, page)
        page_size = max(1, min(page_size, 100))
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        total_pages = (total + page_size - 1) // page_size if total > 0 else 1

        return PaginatedListingsResponse(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            items=[ListingResponse.model_validate(it) for it in items]
        )

    @staticmethod
    def export_csv(
        db: Session,
        search: Optional[str] = None,
        city: Optional[str] = None,
        category: Optional[str] = None,
        source: Optional[str] = None
    ) -> str:
        """
        Generates CSV text representation of filtered listings.
        """
        query = db.query(ListingMaster)

        if search:
            sanitized = sanitize_search_query(search)
            if sanitized:
                query = query.filter(ListingMaster.business_name.ilike(f"%{sanitized}%"))

        if city and city.strip():
            query = query.filter(func.lower(ListingMaster.city) == city.strip().lower())

        if category and category.strip():
            query = query.filter(func.lower(ListingMaster.category) == category.strip().lower())

        if source and source.strip():
            query = query.filter(func.lower(ListingMaster.source) == source.strip().lower())

        records = query.order_by(asc(ListingMaster.id)).all()

        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
        # Headers
        writer.writerow([
            "ID", "Business Name", "Category", "City", "Address", "Phone",
            "Source", "Source ID", "Latitude", "Longitude", "Created At"
        ])

        for r in records:
            writer.writerow([
                r.id,
                r.business_name,
                r.category or "",
                r.city,
                r.address or "",
                r.phone or "",
                r.source,
                r.source_id or "",
                float(r.latitude) if r.latitude is not None else "",
                float(r.longitude) if r.longitude is not None else "",
                r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else ""
            ])

        return output.getvalue()
