"""
Data Collection Engine for Business Listings Intelligence Platform.
Collects genuine business listings from OpenStreetMap (Overpass API with automatic OSM Nominatim and Photon fallbacks).

Usage:
    python -m scraper.collect_data
    python backend/scraper/collect_data.py --cities Bhopal Indore Jaipur Pune Delhi --target 120
"""

import os
import sys
import json
import time
import argparse
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import requests

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from .config import (
        TARGET_CITIES,
        CATEGORIES,
        OVERPASS_ENDPOINTS,
        NOMINATIM_SEARCH_URL,
        PHOTON_SEARCH_URL,
        USER_AGENT,
        REQUEST_TIMEOUT,
        RATE_LIMIT_DELAY,
        MAX_RETRIES,
        BACKOFF_FACTOR,
        RAW_DATA_PATH,
        DATA_DIR,
        DEFAULT_TARGET_PER_CITY
    )
except ImportError:
    from config import (
        TARGET_CITIES,
        CATEGORIES,
        OVERPASS_ENDPOINTS,
        NOMINATIM_SEARCH_URL,
        PHOTON_SEARCH_URL,
        USER_AGENT,
        REQUEST_TIMEOUT,
        RATE_LIMIT_DELAY,
        MAX_RETRIES,
        BACKOFF_FACTOR,
        RAW_DATA_PATH,
        DATA_DIR,
        DEFAULT_TARGET_PER_CITY
    )

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("DataCollector")


class BusinessCollector:
    """Collects genuine business listing data from OpenStreetMap sources."""

    def __init__(self, user_agent: str = USER_AGENT):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": user_agent,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9"
        })
        self.raw_listings: List[Dict[str, Any]] = []
        self.seen_source_ids = set()
        self.active_overpass_endpoint: Optional[str] = None
        self._check_overpass()

    def _check_overpass(self):
        """Quickly tests if any Overpass API mirror is responsive (<= 3s)."""
        logger.info("Probing Overpass API mirrors for availability...")
        test_q = "[out:json][timeout:3];node(1);out;"
        for ep in OVERPASS_ENDPOINTS[:3]:
            try:
                r = self.session.post(ep, data={"data": test_q}, timeout=3)
                if r.status_code == 200:
                    self.active_overpass_endpoint = ep
                    logger.info(f"Overpass mirror online: {ep}")
                    return
            except Exception:
                continue
        logger.warning("All Overpass mirrors timed out or returned errors. Activating OpenStreetMap Nominatim & Photon fallback engines.")

    def fetch_with_retry(self, url: str, params: Optional[Dict] = None, data: Optional[Any] = None, method: str = "GET") -> Optional[requests.Response]:
        """Performs HTTP request with controlled exponential backoff retries."""
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                if method.upper() == "POST":
                    resp = self.session.post(url, data=data, timeout=8)
                else:
                    resp = self.session.get(url, params=params, timeout=8)

                if resp.status_code == 200:
                    return resp
                elif resp.status_code in (429, 502, 503, 504):
                    wait_time = BACKOFF_FACTOR ** attempt
                    logger.warning(f"Got HTTP {resp.status_code} from {url}. Retrying in {wait_time:.1f}s...")
                    time.sleep(wait_time)
                else:
                    logger.debug(f"HTTP {resp.status_code} from {url}")
                    return None
            except (requests.RequestException, TimeoutError) as e:
                wait_time = BACKOFF_FACTOR ** attempt
                logger.debug(f"Request failed ({type(e).__name__}). Retrying in {wait_time:.1f}s...")
                time.sleep(wait_time)
        return None

    def query_overpass_category(self, city: str, city_meta: Dict, category: str, cat_meta: Dict, limit: int = 30) -> List[Dict[str, Any]]:
        """Queries active Overpass API endpoint if available."""
        if not self.active_overpass_endpoint:
            return []

        lat, lon = city_meta["lat"], city_meta["lon"]
        radius = city_meta.get("radius", 15000)
        amenities = cat_meta.get("osm_amenity", [])
        
        union_clauses = [f'node["amenity"="{am}"](around:{radius},{lat},{lon});' for am in amenities]
        query_str = f"""[out:json][timeout:6];\n(\n  {' '.join(union_clauses)}\n);\nout center body {limit};\n"""

        try:
            resp = self.session.post(self.active_overpass_endpoint, data={"data": query_str}, timeout=6)
            if resp.status_code == 200:
                data = resp.json()
                elements = data.get("elements", [])
                results = []
                for el in elements:
                    tags = el.get("tags", {})
                    name = tags.get("name")
                    if not name:
                        continue
                    
                    osm_type = el.get("type", "node")[0].upper()
                    osm_id = el.get("id")
                    source_id = f"OSM:{osm_type}{osm_id}"
                    
                    latitude = el.get("lat") or el.get("center", {}).get("lat")
                    longitude = el.get("lon") or el.get("center", {}).get("lon")
                    phone = tags.get("phone") or tags.get("contact:phone") or tags.get("mobile")
                    
                    addr_parts = [
                        tags.get("addr:housenumber"),
                        tags.get("addr:street"),
                        tags.get("addr:suburb") or tags.get("addr:neighbourhood"),
                        tags.get("addr:city") or city,
                        tags.get("addr:postcode")
                    ]
                    address = ", ".join([str(p) for p in addr_parts if p]) or f"{city}, {city_meta.get('state', '')}"
                    
                    results.append({
                        "business_name": name,
                        "category": category,
                        "city": city,
                        "address": address,
                        "phone": phone,
                        "source": "OpenStreetMap",
                        "source_id": source_id,
                        "latitude": latitude,
                        "longitude": longitude,
                        "collected_at": datetime.utcnow().isoformat() + "Z"
                    })
                return results
        except Exception:
            pass
        return []

    def query_nominatim_category(self, city: str, category: str, keyword: str, limit: int = 25) -> List[Dict[str, Any]]:
        """Queries OpenStreetMap Nominatim Search API for genuine listings with tags & phone."""
        query = f"{keyword} in {city}"
        params = {
            "q": query,
            "format": "json",
            "addressdetails": 1,
            "extratags": 1,
            "limit": limit
        }
        resp = self.fetch_with_retry(NOMINATIM_SEARCH_URL, params=params)
        time.sleep(RATE_LIMIT_DELAY)
        
        if not resp:
            return []

        results = []
        try:
            items = resp.json()
            for it in items:
                display_name = it.get("display_name", "")
                name = display_name.split(",")[0].strip()
                if not name or name.lower() in ("india", city.lower()):
                    continue

                osm_type = (it.get("osm_type") or "node")[0].upper()
                osm_id = it.get("osm_id")
                source_id = f"OSM:{osm_type}{osm_id}"

                extratags = it.get("extratags") or {}
                phone = extratags.get("phone") or extratags.get("contact:phone") or extratags.get("mobile")

                lat = it.get("lat")
                lon = it.get("lon")

                results.append({
                    "business_name": name,
                    "category": category,
                    "city": city,
                    "address": display_name,
                    "phone": phone,
                    "source": "OpenStreetMap",
                    "source_id": source_id,
                    "latitude": float(lat) if lat else None,
                    "longitude": float(lon) if lon else None,
                    "collected_at": datetime.utcnow().isoformat() + "Z"
                })
        except Exception as e:
            logger.debug(f"Nominatim parsing error for {query}: {e}")

        return results

    def query_photon_category(self, city: str, category: str, keyword: str, city_meta: Dict, limit: int = 35) -> List[Dict[str, Any]]:
        """Queries OpenStreetMap Photon Geocoding engine for genuine listings."""
        lat, lon = city_meta["lat"], city_meta["lon"]
        query = f"{keyword} {city}"
        params = {
            "q": query,
            "lat": lat,
            "lon": lon,
            "limit": limit
        }
        resp = self.fetch_with_retry(PHOTON_SEARCH_URL, params=params)
        time.sleep(0.3)

        if not resp:
            return []

        results = []
        try:
            features = resp.json().get("features", [])
            for feat in features:
                props = feat.get("properties", {})
                name = props.get("name")
                if not name:
                    continue

                osm_type = (props.get("osm_type") or "N").upper()
                osm_id = props.get("osm_id")
                source_id = f"OSM:{osm_type}{osm_id}"

                coords = feat.get("geometry", {}).get("coordinates", [None, None])
                longitude, latitude = coords[0], coords[1]

                addr_parts = [
                    props.get("housenumber"),
                    props.get("street"),
                    props.get("locality") or props.get("district"),
                    props.get("city") or city,
                    props.get("postcode")
                ]
                address = ", ".join([str(p) for p in addr_parts if p]) or f"{city}, {props.get('state', '')}"

                results.append({
                    "business_name": name,
                    "category": category,
                    "city": city,
                    "address": address,
                    "phone": None,
                    "source": "OpenStreetMap",
                    "source_id": source_id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "collected_at": datetime.utcnow().isoformat() + "Z"
                })
        except Exception as e:
            logger.debug(f"Photon parsing error: {e}")

        return results

    def collect_city_data(self, city: str, target_count: int = DEFAULT_TARGET_PER_CITY) -> List[Dict[str, Any]]:
        """Collects genuine listings for all target categories within a single city."""
        city_meta = TARGET_CITIES.get(city)
        if not city_meta:
            logger.error(f"City '{city}' not configured in TARGET_CITIES.")
            return []

        logger.info(f"\n==========================================")
        logger.info(f"Collecting listings for city: {city} (Target: ~{target_count})")
        logger.info(f"==========================================")

        city_listings: List[Dict[str, Any]] = []
        per_category_target = max(target_count // len(CATEGORIES), 24)

        for cat_name, cat_meta in CATEGORIES.items():
            cat_listings = []
            logger.info(f"-> Target Category: {cat_name} in {city} (target: {per_category_target})")

            # 1. Attempt Overpass if online
            if self.active_overpass_endpoint:
                overpass_results = self.query_overpass_category(city, city_meta, cat_name, cat_meta, limit=per_category_target)
                for item in overpass_results:
                    sid = item.get("source_id")
                    if sid not in self.seen_source_ids:
                        self.seen_source_ids.add(sid)
                        cat_listings.append(item)

            # 2. Enrich with Nominatim (primary for genuine phone tags + address)
            for kw in cat_meta["keywords"]:
                if len(cat_listings) >= per_category_target:
                    break
                nom_results = self.query_nominatim_category(city, cat_name, kw, limit=20)
                for item in nom_results:
                    sid = item.get("source_id")
                    if sid not in self.seen_source_ids:
                        self.seen_source_ids.add(sid)
                        cat_listings.append(item)

            # 3. Enrich with Photon OSM if needed
            if len(cat_listings) < per_category_target:
                for kw in cat_meta["keywords"]:
                    if len(cat_listings) >= per_category_target:
                        break
                    pho_results = self.query_photon_category(city, cat_name, kw, city_meta, limit=25)
                    for item in pho_results:
                        sid = item.get("source_id")
                        if sid not in self.seen_source_ids:
                            self.seen_source_ids.add(sid)
                            cat_listings.append(item)

            logger.info(f"   Collected {len(cat_listings)} listings for {cat_name} in {city}")
            city_listings.extend(cat_listings)

        logger.info(f"Total collected for {city}: {len(city_listings)} listings\n")
        return city_listings

    def run(self, cities: Optional[List[str]] = None, target_per_city: int = DEFAULT_TARGET_PER_CITY) -> List[Dict[str, Any]]:
        """Runs the complete collection pipeline across requested cities."""
        selected_cities = cities or list(TARGET_CITIES.keys())
        all_listings = []

        start_time = time.time()
        logger.info(f"Starting data collection for {len(selected_cities)} cities: {', '.join(selected_cities)}")

        for city in selected_cities:
            listings = self.collect_city_data(city, target_count=target_per_city)
            all_listings.extend(listings)

        self.raw_listings = all_listings
        elapsed = time.time() - start_time

        logger.info(f"Data collection completed in {elapsed:.1f}s. Total raw records collected: {len(all_listings)}")

        # Save raw data
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(RAW_DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(all_listings, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved raw listings to {RAW_DATA_PATH}")

        return all_listings


def main():
    parser = argparse.ArgumentParser(description="Collect genuine business listings from OpenStreetMap.")
    parser.add_argument("--cities", nargs="+", default=list(TARGET_CITIES.keys()), help="List of cities to collect.")
    parser.add_argument("--target", type=int, default=DEFAULT_TARGET_PER_CITY, help="Target listings per city.")
    args = parser.parse_args()

    collector = BusinessCollector()
    collector.run(cities=args.cities, target_per_city=args.target)


if __name__ == "__main__":
    main()
