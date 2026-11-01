"""
Unit and Integration Tests for Business Listings Intelligence Platform FastAPI Backend.
Uses pytest and FastAPI TestClient with an isolated test database session.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models import Base, ListingMaster
from app.dependencies import get_db

# Create an in-memory SQLite database specifically for tests
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    """Creates a fresh test database for each test function."""
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Overrides get_db dependency to use the isolated test database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# =====================================================================
# 1. Health & Discovery Endpoint Tests
# =====================================================================

def test_api_root(client):
    """Test API discovery endpoint."""
    response = client.get("/api")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "endpoints" in data


def test_health_check(client):
    """Test health endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database_connected" in data


# =====================================================================
# 2. Bulk Insertion & Duplicate Detection Tests
# =====================================================================

def test_bulk_insert_listings(client):
    """Test bulk insertion of new listings."""
    payload = {
        "listings": [
            {
                "business_name": "Apex Hospital",
                "category": "Hospital",
                "city": "Bhopal",
                "address": "Arera Colony, Bhopal",
                "phone": "+91 98260 12345",
                "source": "OpenStreetMap",
                "source_id": "OSM:N1001",
                "latitude": 23.2300,
                "longitude": 77.4200
            },
            {
                "business_name": "Sayaji Hotel",
                "category": "Hotel",
                "city": "Indore",
                "address": "Vijay Nagar, Indore",
                "phone": "+91 73125 67890",
                "source": "OpenStreetMap",
                "source_id": "OSM:N1002",
                "latitude": 22.7500,
                "longitude": 75.8900
            }
        ]
    }
    response = client.post("/api/listings/bulk", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["inserted"] == 2
    assert data["skipped"] == 0
    assert data["failed"] == 0


def test_bulk_insert_duplicate_prevention(client):
    """Test duplicate detection skips existing source_ids."""
    payload = [
        {
            "business_name": "Original Record",
            "category": "Restaurant",
            "city": "Jaipur",
            "address": "MI Road, Jaipur",
            "phone": None,
            "source": "OpenStreetMap",
            "source_id": "OSM:DUPE01",
            "latitude": 26.9100,
            "longitude": 75.8000
        }
    ]
    # First insert
    res1 = client.post("/api/listings/bulk", json=payload)
    assert res1.json()["inserted"] == 1

    # Second insert with duplicate
    res2 = client.post("/api/listings/bulk", json=payload)
    assert res2.json()["inserted"] == 0
    assert res2.json()["skipped"] == 1


def test_bulk_insert_validation_failure(client):
    """Test invalid listing payload rejected."""
    payload = [
        {
            "business_name": "",  # Empty name violates min_length=1
            "category": "School",
            "city": "Pune",
            "source": "OpenStreetMap"
        }
    ]
    response = client.post("/api/listings/bulk", json=payload)
    assert response.status_code == 422  # Pydantic validation error


# =====================================================================
# 3. Listing Query, Search, Filters & Pagination Tests
# =====================================================================

def test_listings_pagination_and_filters(client):
    """Seed data and test pagination, city filter, and search."""
    # Seed 5 records
    seed = [
        {"business_name": "Bhopal Bistro", "category": "Restaurant", "city": "Bhopal", "source": "OSM", "source_id": "1"},
        {"business_name": "Indore IT Hub", "category": "IT Company", "city": "Indore", "source": "OSM", "source_id": "2"},
        {"business_name": "Jaipur Jewels Hotel", "category": "Hotel", "city": "Jaipur", "source": "OSM", "source_id": "3"},
        {"business_name": "Pune Public School", "category": "School", "city": "Pune", "source": "OSM", "source_id": "4"},
        {"business_name": "Delhi Dental Clinic", "category": "Hospital", "city": "Delhi", "source": "OSM", "source_id": "5"},
    ]
    client.post("/api/listings/bulk", json=seed)

    # 1. Total count
    res_all = client.get("/api/listings?page=1&page_size=10")
    assert res_all.status_code == 200
    assert res_all.json()["total"] == 5

    # 2. Filter by City
    res_city = client.get("/api/listings?city=Bhopal")
    assert res_city.json()["total"] == 1
    assert res_city.json()["items"][0]["business_name"] == "Bhopal Bistro"

    # 3. Filter by Category
    res_cat = client.get("/api/listings?category=Hospital")
    assert res_cat.json()["total"] == 1
    assert res_cat.json()["items"][0]["business_name"] == "Delhi Dental Clinic"

    # 4. Search by Name
    res_search = client.get("/api/listings?search=Jewels")
    assert res_search.json()["total"] == 1
    assert res_search.json()["items"][0]["city"] == "Jaipur"

    # 5. Pagination page size limit
    res_page = client.get("/api/listings?page=1&page_size=2")
    assert len(res_page.json()["items"]) == 2
    assert res_page.json()["total_pages"] == 3


# =====================================================================
# 4. Dashboard Summary & Aggregation Tests
# =====================================================================

def test_dashboard_summary_and_aggregations(client):
    """Test dashboard summary KPIs and aggregations."""
    seed = [
        {"business_name": "A", "category": "Hospital", "city": "Bhopal", "phone": "+91 9999999999", "source": "OSM", "source_id": "A1"},
        {"business_name": "B", "category": "Hospital", "city": "Bhopal", "phone": None, "source": "OSM", "source_id": "B1"},
        {"business_name": "C", "category": "Hotel", "city": "Indore", "phone": "+91 8888888888", "source": "OSM", "source_id": "C1"},
    ]
    client.post("/api/listings/bulk", json=seed)

    # Summary
    res_sum = client.get("/api/dashboard/summary")
    assert res_sum.status_code == 200
    s_data = res_sum.json()
    assert s_data["total_listings"] == 3
    assert s_data["total_cities"] == 2
    assert s_data["total_categories"] == 2
    assert s_data["with_phone"] == 2
    assert s_data["without_phone"] == 1
    assert s_data["phone_coverage_percentage"] == 66.67

    # City-wise
    res_city = client.get("/api/dashboard/city-wise")
    assert res_city.status_code == 200
    city_data = res_city.json()
    assert len(city_data) == 2
    assert city_data[0]["city"] == "Bhopal"
    assert city_data[0]["count"] == 2

    # Category-wise
    res_cat = client.get("/api/dashboard/category-wise")
    assert res_cat.status_code == 200
    cat_data = res_cat.json()
    assert len(cat_data) == 2

    # Source-wise
    res_src = client.get("/api/dashboard/source-wise")
    assert res_src.status_code == 200
    assert len(res_src.json()) == 1


# =====================================================================
# 5. Empty Database Behavior
# =====================================================================

def test_empty_database_behavior(client):
    """Test endpoints handle empty database gracefully."""
    res_listings = client.get("/api/listings")
    assert res_listings.status_code == 200
    assert res_listings.json()["total"] == 0
    assert res_listings.json()["items"] == []

    res_sum = client.get("/api/dashboard/summary")
    assert res_sum.status_code == 200
    assert res_sum.json()["total_listings"] == 0
    assert res_sum.json()["phone_coverage_percentage"] == 0.0

    res_cities = client.get("/api/dashboard/city-wise")
    assert res_cities.status_code == 200
    assert res_cities.json() == []


# =====================================================================
# 6. CSV Export Test
# =====================================================================

def test_export_listings_csv(client):
    """Test CSV export endpoint streams CSV data with UTF-8 BOM."""
    client.post("/api/listings/bulk", json=[
        {"business_name": "Export Test Cafe", "category": "Restaurant", "city": "Delhi", "source": "OSM", "source_id": "EXP1"}
    ])
    response = client.get("/api/listings/export?city=Delhi")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    content = response.text
    assert "Export Test Cafe" in content
    assert "Restaurant" in content
    assert "Delhi" in content
