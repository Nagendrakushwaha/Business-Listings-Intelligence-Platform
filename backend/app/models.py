"""
SQLAlchemy ORM Models for Business Listings Intelligence Platform.
Maps exactly to the required MySQL schema for `listing_master`.
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    Numeric,
    DateTime,
    Index,
    UniqueConstraint
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ListingMaster(Base):
    """
    Main Business Listing entity mapping to table `listing_master`.
    """
    __tablename__ = "listing_master"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    business_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=True, index=True)
    city = Column(String(100), nullable=False, index=True)
    address = Column(Text, nullable=True)
    phone = Column(String(30), nullable=True)
    source = Column(String(100), nullable=False, index=True)
    source_id = Column(String(150), nullable=True)
    latitude = Column(Numeric(10, 7), nullable=True)
    longitude = Column(Numeric(10, 7), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)

    __table_args__ = (
        UniqueConstraint("source", "source_id", name="unique_source_listing"),
        Index("idx_city", "city"),
        Index("idx_category", "category"),
        Index("idx_source", "source"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "business_name": self.business_name,
            "category": self.category,
            "city": self.city,
            "address": self.address,
            "phone": self.phone,
            "source": self.source,
            "source_id": self.source_id,
            "latitude": float(self.latitude) if self.latitude is not None else None,
            "longitude": float(self.longitude) if self.longitude is not None else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
