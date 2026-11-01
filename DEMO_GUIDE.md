# Video Demonstration & Evaluation Script (3–5 Minutes)
## Business Listings Intelligence Platform
**Candidate Technical Assessment — Honeybee Digital Data Science Internship**

---

### Segment 1: Executive Overview & System Architecture (0:00 – 0:30)
- **Visual**: Show the React Dashboard on `http://localhost:5173/` in light theme, showcasing the 6 KPI cards and interactive charts.
- **Script**:
  > *"Hello! My name is [Your Name], and this is my presentation for the Data Science Internship technical assessment at Honeybee Digital. I have designed and developed the **Business Listings Intelligence Platform** — a production-ready, full-stack application built to collect, cleanse, store, manage, and visualize commercial establishments across 5 major Indian metropolitan areas: Bhopal, Indore, Jaipur, Pune, and Delhi.*
  > *Our architecture follows a clean 3-tier design: a Python 3.13 data ingestion and normalization pipeline, a persistent MySQL database with connection pooling, a FastAPI REST backend with Pydantic validation and Swagger UI, and a React + Vite + Tailwind CSS analytics dashboard."*

---

### Segment 2: Ethical Data Collection & Cleaning Engine (0:30 – 1:15)
- **Visual**: Open VS Code or terminal showing `backend/scraper/collect_data.py` and `backend/scraper/clean_data.py`. Highlight `data/business_listings.csv` (857 rows) and `data/data_quality_report.json`.
- **Script**:
  > *"The data collection engine was designed around two core principles: legal compliance and authentic data integrity. Our primary data source is OpenStreetMap using Overpass API queries, with intelligent failover to OSM Nominatim and Photon geocoding engines.*
  > *Across the 5 cities, we targeted 5 core sectors: Restaurants, Hospitals, Hotels, Schools, and IT companies. We surpassed the assignment's 500-record threshold by gathering **882 raw listings**, which our preprocessing pipeline cleaned down to **857 deduplicated, validated records**.*
  > *Notice our strict **Zero-Fabrication Guarantee**: where phone numbers were not publicly listed in OSM tags, they are explicitly preserved as `NULL` rather than synthesized. Every listing preserves its original OpenStreetMap identifier, such as `OSM:N7518423169`, ensuring 100% data traceability under the Open Database License."*

---

### Segment 3: MySQL Database & FastAPI Backend (1:15 – 2:00)
- **Visual**: Switch browser tab to `http://localhost:8000/docs` (Swagger UI). Execute `GET /api/dashboard/summary` and `POST /api/listings/bulk`.
- **Script**:
  > *"Here is our FastAPI backend, running with Uvicorn and SQLAlchemy. The relational schema is centered around `listing_master` in MySQL, equipped with composite unique constraints on `(source, source_id)` and indexes on `city`, `category`, and `source`.*
  > *Let's test the interactive Swagger documentation. When we execute `GET /api/dashboard/summary`, the API returns live aggregated metrics: 857 businesses across 5 cities and 5 categories, with 148 verified contact numbers.*
  > *Our `POST /api/listings/bulk` endpoint implements atomic transactions: if a duplicate listing is received, the service detects it and returns the count of inserted versus skipped records without failing the batch."*

---

### Segment 4: React Dashboard, Charts & Directory (2:00 – 3:30)
- **Visual**: Return to `http://localhost:5173/`. Toggle between dark and light themes. Filter by city "Bhopal" and category "Hospital". Sort by Business Name. Paginate through records.
- **Script**:
  > *"Now let's explore the frontend. Built with React, Vite, Tailwind CSS, Recharts, and Lucide icons, it provides a SaaS analytics experience.*
  > *At the top, our 6 KPI cards dynamically reflect backend state: Total Businesses, Cities, Categories, Data Sources, and phone distribution.*
  > *Below, our Recharts visualizations include: an interactive City Distribution bar chart and a Category Composition donut chart. Hovering reveals custom tooltips with exact counts and directory shares.*
  > *In the Directory Explorer table, we support real-time debounce search, multi-column sorting, and multi-criteria filters. For example, filtering by city 'Bhopal' and category 'Hospital' instantly isolates medical establishments, complete with coordinates, structured addresses, and phone badges.*
  > *Let's also look at the City Analytics and Category Analytics views on the sidebar, which provide deep dives and regional ranking tables."*

---

### Segment 5: CSV Export & Data Quality Scorecard (3:30 – 4:00)
- **Visual**: Click "Export CSV". Show the downloaded file opening in Excel or text editor. Switch to the "Data Quality" tab.
- **Script**:
  > *"A mandatory assessment requirement is seamless CSV export. Clicking 'Export CSV' triggers our FastAPI streaming endpoint, which generates an Excel-compatible CSV with UTF-8 BOM encoding and clear column headers.*
  > *On the Data Quality page, we display our automated audit report: total raw records collected (882), deduplicated records filtered (25), coordinate bounds validation (0 invalid), and verified phone coverage (17.27%). Every metric is grounded in reproducible pipeline outputs."*

---

### Segment 6: Engineering Reflections & Next Steps (4:00 – 5:00)
- **Visual**: Show GitHub repository files, test suite execution in terminal (`pytest`), and the comprehensive `README.md`.
- **Script**:
  > *"To ensure reliability, we implemented a pytest integration suite covering pagination, search, validation, empty database behavior, and duplicate prevention.*
  > *During development, our biggest technical hurdle was handling intermittent rate limits and public Overpass server latency. We solved this by implementing an adaptive failover architecture with exponential backoff and secondary OSM geocoding APIs.*
  > *For future iterations, we could integrate geospatial radius search using MySQL spatial indexes (ST_Distance), implement scheduled cron jobs for automatic directory refreshes, and incorporate review sentiment analysis.*
  > *Thank you to the Honeybee Digital team for reviewing my submission. I look forward to discussing the architecture during the interview!"*

