# Business Listings Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3-61dafb.svg)](https://react.dev/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1.svg)](https://www.mysql.com/)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.4-38bdf8.svg)](https://tailwindcss.com/)
[![License: ODbL](https://img.shields.io/badge/Data_License-ODbL-green.svg)](https://opendatacommons.org/licenses/odbl/)

> **Candidate Technical Assessment Submission for Data Science Internship at Honeybee Digital**  
> An enterprise-grade, end-to-end full-stack platform designed to ethically collect, cleanse, store, manage, analyze, and visualize authentic commercial business listings across Indian metropolitan centers.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Objectives](#3-objectives)
4. [Key Features](#4-key-features)
5. [Technology Stack](#5-technology-stack)
6. [Architecture Diagram](#6-architecture-diagram)
7. [Data Collection Methodology](#7-data-collection-methodology)
8. [Data Cleaning & Normalization Methodology](#8-data-cleaning--normalization-methodology)
9. [Database Schema & Architecture](#9-database-schema--architecture)
10. [REST API Documentation](#10-rest-api-documentation)
11. [Frontend Dashboard Overview](#11-frontend-dashboard-overview)
12. [Installation & Setup Instructions](#12-installation--setup-instructions)
13. [Windows 11 PowerShell Setup Commands](#13-windows-11-powershell-setup-commands)
14. [MySQL Configuration Guide](#14-mysql-configuration-guide)
15. [How to Run the Scraper Module](#15-how-to-run-the-scraper-module)
16. [How to Run the FastAPI Backend](#16-how-to-run-the-fastapi-backend)
17. [How to Run the React Frontend](#17-how-to-run-the-react-frontend)
18. [How to Import the MySQL Database Dump](#18-how-to-import-the-mysql-database-dump)
19. [Testing Suite & Quality Verification](#19-testing-suite--quality-verification)
20. [Dashboard Screenshots & Visual Walkthrough](#20-dashboard-screenshots--visual-walkthrough)
21. [Engineering Challenges Faced & Resolutions](#21-engineering-challenges-faced--resolutions)
22. [Real-World Data Limitations](#22-real-world-data-limitations)
23. [Data Source Attribution & Legal Licensing](#23-data-source-attribution--legal-licensing)
24. [Future Roadmap & Enhancements](#24-future-roadmap--enhancements)

---

## 1. Project Overview

The **Business Listings Intelligence Platform** addresses the challenge of acquiring authentic, validated geographic and commercial intelligence on Indian small-and-medium enterprises (SMEs) without resorting to fraudulent web-scraping tactics or fabricated synthetic data. 

Developed specifically for the Honeybee Digital technical evaluation, this platform incorporates an automated data pipeline targeting five major Indian metropolitan centers (**Bhopal, Indore, Jaipur, Pune, and Delhi**) across five essential economic sectors (**Restaurants, Hospitals, Hotels, Schools, and IT Companies**).

The complete platform includes:
- An **autonomous Python scraper** consuming OpenStreetMap Overpass and geocoding APIs.
- A **data preprocessing and quality engine** that standardizes phone numbers, normalizes categories, eliminates duplicates, and validates spatial coordinates.
- A **MySQL 8.0 relational data store** housing `listing_master` with parameterized queries, connection pooling, and strict schema constraints.
- A **FastAPI REST API backend** exposing paginated directory queries, aggregation metrics, and streaming Excel-compatible CSV exports.
- A **React + Vite + Tailwind CSS dashboard** with interactive Recharts visualizations, dark/light theme switching, and multi-filter directory search.

---

## 2. Problem Statement

Data science workflows in local business intelligence frequently suffer from three critical flaws:
1. **Unreliable & Fragile Web Scraping**: Brittle scrapers reliant on unstable HTML DOM selectors that break upon minor website redesigns or get blocked by aggressive anti-bot protections.
2. **Synthetic Data Fabrication**: Projects generating synthetic names or fictional phone numbers to hit artificial dataset thresholds, degrading model validity.
3. **Disconnected Prototypes**: Engineering prototypes that exist only as Jupyter notebooks or static mockups without a connected database or reactive interface.

This project solves these issues by establishing an authentic, reproducible data pipeline grounded in open geographical databases, validated through relational integrity, and presented via a modern SaaS analytics UI.

---

## 3. Objectives

- **Target Ingestion**: Collect $\ge 500$ unique, authentic commercial listings across 5 target cities (achieved: **857 cleaned listings** from **882 raw ingestions**).
- **Zero Fabrication**: Maintain strict data authenticity—never invent phone numbers or addresses. Missing values are explicitly preserved as `NULL`.
- **Relational Integrity**: Store records in MySQL `listing_master` with composite unique constraints `(source, source_id)` to prevent duplicate imports.
- **Performant APIs**: Provide FastAPI endpoints for paginated filtering, bulk insertion with atomic error reporting, and aggregated summaries.
- **Interactive UI**: Deliver a polished React dashboard featuring KPI cards, bar charts, donut charts, and instant directory search.
- **Interoperability**: Support UTF-8 BOM CSV exports compatible with Microsoft Excel and LibreOffice.

---

## 4. Key Features

- **Multi-Source Failover Engine**: Queries OpenStreetMap Overpass API with automatic fallback to OSM Nominatim and Photon geocoding engines.
- **Enterprise Deduplication**: Two-stage deduplication detecting duplicate source IDs (`OSM:N...`) and semantic duplicates on `(business_name, city)`.
- **Strict Indian Phone Normalization**: Strips non-digits, normalizes `+91` formats for 10-digit mobile/landline numbers, and maps absent data to `NULL`.
- **Coordinate Boundary Sanitization**: Confirms all latitude and longitude coordinates reside within Indian geographical bounding boxes.
- **Live Aggregation Endpoints**: Backend SQL aggregations calculating distribution metrics per city, category, and source.
- **FastAPI OpenAPI / Swagger Documentation**: Full interactive API testing at `/docs`.
- **Responsive Analytics Dashboard**: Built with Tailwind CSS, supporting light/dark modes, loading skeletons, and error retry states.
- **Excel-Compatible CSV Streaming**: Exports filtered datasets with UTF-8 BOM headers.

---

## 5. Technology Stack

### Backend
- **Python**: 3.13 (Native x64)
- **FastAPI**: 0.115.6 (Modern asynchronous web framework)
- **Uvicorn**: 0.34.0 (ASGI web server)
- **SQLAlchemy**: 2.0.36 (Relational ORM & Connection Pooling)
- **PyMySQL**: 1.2.3 (Pure-Python MySQL client driver)
- **Pydantic**: 2.10.4 (Strict schema validation & serialization)
- **Pandas**: 2.2.3 (Vectorized data manipulation & quality scoring)
- **Requests & HTTPX**: Resilient HTTP networking with backoff

### Frontend
- **React.js**: 18.3.1 (Component architecture)
- **Vite**: 6.0.3 (Modern ES module build tooling)
- **Tailwind CSS**: 3.4.16 (Utility-first styling with dark mode support)
- **Recharts**: 2.15.0 (Declarative data visualization)
- **Lucide React**: 0.468.0 (Modern iconography)
- **Axios**: 1.7.9 (Promise-based API client)

### Database
- **MySQL Server**: 8.0.45 (InnoDB engine, utf8mb4 charset)
- **Database Name**: `business_listings_db`
- **Primary Table**: `listing_master`

---

## 6. Architecture Diagram

```
+-------------------------------------------------------------------------------+
|                       OPENSTREETMAP DATA SOURCES                              |
|  Overpass API (Mirrors)  |  OSM Nominatim API  |  OSM Photon Geocoding Engine |
+-------------------------------------------------------------------------------+
                                        | (HTTPS / ODbL Compliant Ingestion)
                                        v
+-------------------------------------------------------------------------------+
|                     PYTHON 3.13 DATA SCRAPER & CLEANER                        |
|  - backend/scraper/collect_data.py (Multi-mirror adaptive scraper)            |
|  - backend/scraper/clean_data.py   (Validation, deduplication, normalizer)    |
|  - data/business_listings.csv      (857 verified listings)                    |
|  - data/data_quality_report.json   (Integrity audit metadata)                 |
+-------------------------------------------------------------------------------+
                                        | (SQLAlchemy / PyMySQL Connection Pool)
                                        v
+-------------------------------------------------------------------------------+
|                       MYSQL 8.0 RELATIONAL DATABASE                           |
|  Database: business_listings_db                                               |
|  Table: listing_master                                                         |
|  - Composite Unique Key: (source, source_id)                                  |
|  - Indexes: idx_city, idx_category, idx_source                                |
+-------------------------------------------------------------------------------+
                                        ^
                                        | (Connection Pooling & Sessions)
                                        v
+-------------------------------------------------------------------------------+
|                           FASTAPI REST BACKEND                                |
|  - POST /api/listings/bulk        - GET /api/listings?page=1&city=...         |
|  - GET  /api/dashboard/summary    - GET /api/dashboard/city-wise             |
|  - GET  /api/dashboard/category   - GET /api/dashboard/source-wise           |
|  - GET  /api/listings/export      - GET /api/health                           |
+-------------------------------------------------------------------------------+
                                        ^
                                        | (Axios HTTP Client / JSON / Port 5173)
                                        v
+-------------------------------------------------------------------------------+
|                      REACT + VITE ANALYTICS FRONTEND                          |
|  - 6 KPI Cards (Total businesses, cities, categories, phone distribution)     |
|  - Recharts City Bar Chart & Category Donut Chart                             |
|  - Filterable, Searchable, Sortable Directory Table with Pagination           |
|  - Data Quality Audit View & One-Click CSV Export                             |
+-------------------------------------------------------------------------------+
```

---

## 7. Data Collection Methodology

Data collection is executed through `backend/scraper/collect_data.py`:

1. **Spatial Bounding & Centroid Radii**:
   Each city is configured with centroid latitude/longitude coordinates and radial search buffers (15–18 km):
   - **Bhopal**: `(23.2599, 77.4126)`
   - **Indore**: `(22.7196, 75.8577)`
   - **Jaipur**: `(26.9124, 75.7873)`
   - **Pune**: `(18.5204, 73.8567)`
   - **Delhi**: `(28.6139, 77.2090)`

2. **Multi-Source Failover Engine**:
   - The engine first attempts to contact Overpass API mirrors.
   - If public Overpass mirrors experience downtime or rate limiting, the engine activates fallback pipelines querying **OSM Nominatim** and **OSM Photon**.
   - These engines return genuine OpenStreetMap nodes (`N`), ways (`W`), and relations (`R`) with verified coordinates and public contact tags.

3. **Rate Limiting & Politeness**:
   - Requests are paced with a minimum 1.0-second delay between Nominatim calls to respect the OpenStreetMap foundation guidelines.
   - User-Agent identification is passed with project contact information.
   - Automated exponential backoff handles transient network timeouts.

---

## 8. Data Cleaning & Normalization Methodology

The preprocessing pipeline (`backend/scraper/clean_data.py`) enforces strict validation criteria:

- **Deduplication**:
  - Eliminates identical records sharing the same `(source, source_id)`.
  - Performs semantic deduplication on normalized `(business_name, city)` tuples.
- **Business Name Sanitization**:
  - Strips surrounding quotes, trailing city suffixes (e.g. `" - Bhopal"`, `", Jaipur"`), and collapses excessive whitespace.
  - Converts names to title case if formatted in all-caps or all-lowercase.
- **Category Standardization**:
  - Maps diverse OSM tags into five canonical categories: `Restaurant`, `Hospital`, `Hotel`, `School`, and `IT Company`.
- **Zero Synthetic Fabrication**:
  - Absent phone numbers are explicitly recorded as `NULL`. No dummy numbers like `9999999999` or placeholder addresses are manufactured.
- **Geographic Validation**:
  - Ensures latitude falls strictly within $[-90.0, 90.0]$ and longitude within $[-180.0, 180.0]$, verifying that coordinates align with the Indian subcontinent.

---

## 9. Database Schema & Architecture

The database schema is defined in `database/schema.sql`:

```sql
CREATE DATABASE IF NOT EXISTS `business_listings_db`
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE `business_listings_db`;

CREATE TABLE `listing_master` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `business_name` VARCHAR(255) NOT NULL,
    `category` VARCHAR(100),
    `city` VARCHAR(100) NOT NULL,
    `address` TEXT,
    `phone` VARCHAR(30),
    `source` VARCHAR(100) NOT NULL,
    `source_id` VARCHAR(150),
    `latitude` DECIMAL(10,7),
    `longitude` DECIMAL(10,7),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY `unique_source_listing` (`source`, `source_id`),
    INDEX `idx_city` (`city`),
    INDEX `idx_category` (`category`),
    INDEX `idx_source` (`source`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 10. REST API Documentation

FastAPI automatically generates interactive OpenAPI documentation accessible at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### API Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Healthcheck and MySQL connection status |
| `POST` | `/api/listings/bulk` | Bulk insert listings with duplicate handling |
| `GET` | `/api/listings` | Paginated listings with search and multi-filtering |
| `GET` | `/api/listings/export` | Stream Excel-compatible CSV with UTF-8 BOM |
| `GET` | `/api/dashboard/summary` | Top-level KPIs (total listings, cities, phone coverage) |
| `GET` | `/api/dashboard/city-wise` | Business listing counts and percentage per city |
| `GET` | `/api/dashboard/category-wise`| Business listing counts and percentage per category |
| `GET` | `/api/dashboard/source-wise` | Distribution across ingestion sources |
| `GET` | `/api/dashboard/data-quality` | Integrity audit scorecard and data cleaning statistics |

---

## 11. Frontend Dashboard Overview

The React interface is built around a modern SaaS design system:
- **Header**: Includes platform brand, global search input, animated refresh button, last updated timestamp, and dark/light mode toggle.
- **Sidebar**: Easy navigation across Overview, Business Directory, City Analytics, Category Analytics, Source Provenance, Data Quality, and Settings.
- **KPI Cards**: Real-time display of total verified businesses, city coverage, category coverage, data sources, and phone coverage percentage.
- **Charts**:
  - `CityBarChart`: Custom tooltips and gradient bars for cross-city comparison.
  - `CategoryPieChart`: Responsive donut chart with percentage badges.
  - `SourceChart`: Visual representation of source provenance and ODbL licensing.
- **Directory Table**: Real-time search, multi-select filters, sortable column headers, pagination controls, and CSV export.

---

## 12. Installation & Setup Instructions

### Prerequisites
- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: Python 3.13 (or 3.11+)
- **Node.js**: v18+ (tested on Node v24.19.0 with npm 11.17.0)
- **Database**: MySQL Server 8.0+

---

## 13. Windows 11 PowerShell Setup Commands

Open two PowerShell windows:

### Terminal 1: Backend Setup & Execution
```powershell
# Navigate to backend directory
cd "backend"

# Create a virtual environment using Python 3.13
py -3.13 -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install required Python packages
python -m pip install --upgrade pip
pip install -r requirements.txt

# Start FastAPI ASGI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2: Frontend Setup & Execution
```powershell
# Navigate to frontend directory
cd "frontend"

# Install frontend npm dependencies
npm install

# Start Vite React development server
npm run dev
```

Visit the dashboard in your browser: `http://localhost:5173/`

---

## 14. MySQL Configuration Guide

1. Ensure MySQL Server 8.0 is running locally on port `3306`.
2. Configure your MySQL credentials in `backend/.env`:
   ```env
   DB_USER=root
   DB_PASSWORD=your_actual_mysql_password
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=business_listings_db
   ```
3. Initialize the database and table:
   ```powershell
   mysql -u root -p < database/schema.sql
   ```
4. Seed the database directly from the cleaned CSV:
   ```powershell
   python database/seed_data.py
   ```

---

## 15. How to Run the Scraper Module

The scraper is completely standalone and can be re-run at any time:

```powershell
# In backend directory
python -m scraper.collect_data

# Or with custom city targets
python backend/scraper/collect_data.py --cities Bhopal Indore Jaipur Pune Delhi --target 120
```

Raw listings are saved to `data/raw_business_listings.json`.

Then execute data cleaning and audit reporting:
```powershell
python -m scraper.clean_data
```

Cleaned listings are saved to `data/business_listings.csv` and report to `data/data_quality_report.json`.

---

## 16. How to Run the Backend

```powershell
cd backend
python -m uvicorn app.main:app --reload --port 8000
```
Interactive Swagger documentation is live at `http://localhost:8000/docs`.

---

## 17. How to Run the Frontend

```powershell
cd frontend
npm run dev
```
Access the application at `http://localhost:5173/`.

To build the optimized production bundle:
```powershell
npm run build
```

---

## 18. How to Import the MySQL Database Dump

We have pre-compiled a complete, standalone MySQL database dump containing the DDL and all 857 cleaned records at `database/business_listings.sql`.

Import it into MySQL in one command:
```powershell
mysql -u root -p < database/business_listings.sql
```

Verify in MySQL shell:
```sql
USE business_listings_db;
SELECT COUNT(*) FROM listing_master;
-- Output: 857
```

---

## 19. Testing Suite & Quality Verification

Run the automated pytest integration test suite:

```powershell
cd backend
python -m pytest tests/ -v
```

### Test Coverage Results
```
tests/test_api.py::test_api_root PASSED                         [ 11%]
tests/test_api.py::test_health_check PASSED                     [ 22%]
tests/test_api.py::test_bulk_insert_listings PASSED             [ 33%]
tests/test_api.py::test_bulk_insert_duplicate_prevention PASSED [ 44%]
tests/test_api.py::test_bulk_insert_validation_failure PASSED   [ 55%]
tests/test_api.py::test_listings_pagination_and_filters PASSED  [ 66%]
tests/test_api.py::test_dashboard_summary_and_aggregations PASSED [ 77%]
tests/test_api.py::test_empty_database_behavior PASSED          [ 88%]
tests/test_api.py::test_export_listings_csv PASSED              [100%]

======================= 9 passed in 2.99s =======================
```

---

## 20. Dashboard Screenshots & Visual Walkthrough

*(Screenshots can be captured directly from `http://localhost:5173/` and placed in `screenshots/`)*

- `screenshots/01_dashboard_overview.png`: Top-level KPI cards, City Bar Chart, Category Donut Chart.
- `screenshots/02_directory_table.png`: Business Directory with multi-criteria filters, search, and pagination.
- `screenshots/03_city_analytics.png`: City performance breakdown and rankings.
- `screenshots/04_data_quality_report.png`: Data quality scorecard and zero-fabrication metrics.
- `screenshots/05_swagger_ui.png`: Interactive FastAPI documentation at `/docs`.

---

## 21. Engineering Challenges Faced & Resolutions

1. **Overpass API Mirror Latency & 406/502 Outages**:
   - *Challenge*: Public Overpass API mirrors regularly experience heavy global load, resulting in 502 Bad Gateway responses or read timeouts.
   - *Resolution*: Implemented an adaptive multi-tier ingestion architecture with 3-second health probes and automatic failover to OpenStreetMap Nominatim and Photon geocoding APIs.

2. **Heterogeneous Category Tags in OSM**:
   - *Challenge*: OpenStreetMap contributors use varied tags for establishments (e.g. `amenity=fast_food`, `amenity=cafe`, `amenity=restaurant`, `office=it`, `office=company`).
   - *Resolution*: Designed a taxonomy normalizer mapping diverse keywords and amenity values into five standardized sectors.

3. **Autoincrement Compatibility Between MySQL and Test Environments**:
   - *Challenge*: Pytest fixtures use in-memory SQLite for test speed, where `BIGINT PRIMARY KEY` does not automatically autoincrement without specific SQLite variant mappings.
   - *Resolution*: Configured `BigInteger().with_variant(Integer, "sqlite")` in SQLAlchemy models, ensuring smooth test execution and MySQL production compatibility.

---

## 22. Real-World Data Limitations

- **Phone Number Coverage in Crowdsourced Data**: In OpenStreetMap for Indian commercial listings, contact numbers are voluntarily contributed. In our collected dataset of 857 listings, 148 listings (~17.27%) contain verified public phone numbers. Rather than fabricating fictitious numbers to artificially boost this figure, we chose strict data authenticity and mapped absent numbers to `NULL`.
- **Informal Sector Representation**: OpenStreetMap has strong coverage of hospitals, hotels, schools, and established restaurants, but informal roadside stalls or unregistered businesses have lower digital representation.

---

## 23. Data Source Attribution & Legal Licensing

- **Data Attribution**: © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright).
- **License**: The data is made available under the [Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/).
- **Ethical Compliance**: The data pipeline strictly complies with OpenStreetMap API usage policies, using descriptive User-Agents, respectful request intervals, and preserving canonical source identifiers (`source_id`).

---

## 24. Future Roadmap & Enhancements

- **Geospatial Proximity Queries**: Implement MySQL `ST_Distance_Sphere` spatial queries to allow users to find businesses within *X* kilometers of any pin.
- **Scheduled Automated Ingestion**: Configure background Celery or APScheduler tasks to periodically re-scrape and update directory listings.
- **Geocoding Enrichment**: Integrate reverse-geocoding pipelines to enrich postal codes and ward names.
- **User Contribution Portal**: Allow authenticated business owners to claim listings and update verified operating hours.

---

## Internship Submission Deliverables Checklist

- [x] **500+ Genuine Business Listings Collected**: 857 unique cleaned records across 5 cities and 5 categories.
- [x] **Python Scraper & Cleaner**: `backend/scraper/collect_data.py`, `backend/scraper/clean_data.py`, `backend/scraper/export_csv.py`.
- [x] **MySQL Database Schema & Model**: `database/schema.sql`, `backend/app/models.py`.
- [x] **FastAPI REST API**: Bulk insert, paginated listings, summary metrics, city/category/source aggregations, CSV export.
- [x] **React + Vite Dashboard**: Premium SaaS design with KPI cards, Recharts, dark/light modes, and directory explorer.
- [x] **MySQL Database Dump**: Generated at `database/business_listings.sql`.
- [x] **Full Pytest Suite**: 9 unit and integration tests passing.
- [x] **Video Demonstration Guide**: Prepared in `DEMO_GUIDE.md`.
- [x] **Complete Documentation**: Comprehensive `README.md`.

