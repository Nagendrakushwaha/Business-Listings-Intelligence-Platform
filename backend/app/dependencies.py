"""
FastAPI route dependencies.
"""

from app.database import get_db

# Re-export get_db as standard session dependency
__all__ = ["get_db"]

