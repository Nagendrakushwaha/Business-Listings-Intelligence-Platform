"""
Health check and system status endpoint.
"""

from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.database import check_db_connection
from app.schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=HealthResponse)
def get_health():
    """Returns application health status and MySQL database connectivity."""
    is_connected, version = check_db_connection()
    return HealthResponse(
        status="healthy" if is_connected else "degraded",
        database_connected=is_connected,
        database_version=version if is_connected else None,
        timestamp=datetime.utcnow()
    )
