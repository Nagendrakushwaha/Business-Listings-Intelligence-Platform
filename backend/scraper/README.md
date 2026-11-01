# Business Listings Intelligence Platform — Scraper Module

This module is responsible for automated, compliant, and ethical data collection and preprocessing of genuine business listings across Indian metropolitan cities from **OpenStreetMap (OSM)**.

---

## Architecture & Data Flow

```
+-----------------------------------------------------------+
|              Data Collection Pipeline                     |
+-----------------------------------------------------------+
                             |
         +-------------------+-------------------+
         |                                       |
  [Overpass API]                        [OSM Nominatim / Photon]
 (Mirror Failover)                         (Resilient Fallback)
         |                                       |
         +-------------------+-------------------+
                             |
                             v
               Raw JSON Storage (data/raw_business_listings.json)
                             |
                             v
               Data Cleaning & Normalization Engine
                  - Deduplication (source_id + Name/City)
                  - Category Standardisation (5 core categories)
                  - Phone Normalization (+91 format, NULL if missing)
                  - Coordinate Validation
                  - Zero Synthetic Data Manufacture
                             |
                             v
               Cleaned Dataset (data/business_listings.csv)
                             +
               Quality Audit (data/data_quality_report.json)
```

---

## Target Cities & Categories

- **Cities (5)**: Bhopal, Indore, Jaipur, Pune, Delhi
- **Categories (5)**: Restaurants, Hospitals, Hotels, Schools, IT Companies
- **Overall Target**: $\ge 500$ unique genuine business listings (~100–120 per city)

---

## Key Files

| File | Purpose |
| :--- | :--- |
| `config.py` | Central configuration: cities, coordinates, endpoints, categories, rate limits. |
| `collect_data.py` | Multi-source scraper with retry backoff, Overpass mirrors, and Nominatim/Photon fallbacks. |
| `clean_data.py` | Data normalization, deduplication, validation, and Data Quality Report generator. |
| `export_csv.py` | Filterable CSV export utility with UTF-8 BOM encoding for Microsoft Excel compatibility. |

---

## How to Run Independently

### 1. Collect Data
```powershell
# From the backend directory
python -m scraper.collect_data

# Or with custom city selection
python backend/scraper/collect_data.py --cities Bhopal Indore Jaipur Pune Delhi --target 120
```

### 2. Clean & Validate Data
```powershell
python -m scraper.clean_data
```

### 3. Export Filtered CSV
```powershell
python -m scraper.export_csv --city Bhopal --output data/bhopal_listings.csv
```

---

## Ethical Scraping & Licensing Compliance
- Respects OpenStreetMap **ODbL (Open Database License)**.
- Complies with OSM Nominatim usage policy (1 request/sec rate limiting, descriptive User-Agent).
- **Zero Synthetic Fabrication**: Missing phone numbers are explicitly preserved as `NULL` instead of generating fake contact details.
