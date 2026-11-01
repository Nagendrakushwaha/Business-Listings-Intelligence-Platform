"""
Configuration settings for the Business Listings Intelligence Data Scraper.
Supports configurable cities, categories, Overpass endpoints, and fallbacks.
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "raw_business_listings.json"
CLEAN_DATA_PATH = DATA_DIR / "business_listings.csv"
DATA_QUALITY_REPORT_JSON = DATA_DIR / "data_quality_report.json"
DATA_QUALITY_REPORT_MD = DATA_DIR / "data_quality_report.md"

# Target Cities with geographical bounding boxes and center coordinates
TARGET_CITIES = {
    "Bhopal": {
        "lat": 23.2599,
        "lon": 77.4126,
        "radius": 15000,
        "bbox": [23.15, 77.30, 23.35, 77.55],
        "state": "Madhya Pradesh"
    },
    "Indore": {
        "lat": 22.7196,
        "lon": 75.8577,
        "radius": 15000,
        "bbox": [22.65, 75.78, 22.80, 75.95],
        "state": "Madhya Pradesh"
    },
    "Jaipur": {
        "lat": 26.9124,
        "lon": 75.7873,
        "radius": 15000,
        "bbox": [26.80, 75.70, 27.02, 75.92],
        "state": "Rajasthan"
    },
    "Pune": {
        "lat": 18.5204,
        "lon": 73.8567,
        "radius": 16000,
        "bbox": [18.42, 73.75, 18.62, 73.98],
        "state": "Maharashtra"
    },
    "Delhi": {
        "lat": 28.6139,
        "lon": 77.2090,
        "radius": 18000,
        "bbox": [28.48, 77.05, 28.75, 77.35],
        "state": "Delhi"
    }
}

# Target Business Categories and their OSM tag mappings & search keywords
CATEGORIES = {
    "Restaurant": {
        "osm_amenity": ["restaurant", "cafe", "fast_food"],
        "keywords": ["restaurant", "cafe", "dhaba", "fine dining"],
        "display_name": "Restaurants"
    },
    "Hospital": {
        "osm_amenity": ["hospital", "clinic"],
        "keywords": ["hospital", "clinic", "nursing home", "healthcare"],
        "display_name": "Hospitals"
    },
    "Hotel": {
        "osm_amenity": ["hotel", "guest_house"],
        "keywords": ["hotel", "resort", "guest house", "lodge"],
        "display_name": "Hotels"
    },
    "School": {
        "osm_amenity": ["school", "college"],
        "keywords": ["school", "public school", "academy", "college"],
        "display_name": "Schools"
    },
    "IT Company": {
        "osm_amenity": ["it", "company"],
        "keywords": ["software company", "it services", "tech company", "software solutions"],
        "display_name": "IT Companies"
    }
}

# Overpass API mirrors for fallback resilience
OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
    "https://overpass.osm.ch/api/interpreter"
]

# Official OpenStreetMap Nominatim and Photon Search API endpoints
NOMINATIM_SEARCH_URL = "https://nominatim.openstreetmap.org/search"
PHOTON_SEARCH_URL = "https://photon.komoot.io/api/"

# Request Settings
USER_AGENT = "BusinessListingsIntelligencePlatform/1.0 (academic research assessment; contact: student@honeybeedigital.internal)"
REQUEST_TIMEOUT = 15
RATE_LIMIT_DELAY = 1.0  # seconds between external API calls to respect OpenStreetMap guidelines
MAX_RETRIES = 3
BACKOFF_FACTOR = 1.5

# Targets
DEFAULT_TARGET_PER_CITY = 120
TOTAL_MINIMUM_TARGET = 500

