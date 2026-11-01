"""
Main FastAPI Application Entry Point.
Configures CORS, routers, OpenAPI metadata, and lifecycle events.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.routes import health, listings, dashboard
from app.database import init_db
from app.utils.logger import api_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle handler."""
    api_logger.info("Initializing Business Listings Intelligence Platform API...")
    # Safe DB initialization
    try:
        init_db()
    except Exception as e:
        api_logger.warning(f"Database auto-initialization skipped or deferred: {e}")
    yield
    api_logger.info("Shutting down Business Listings Intelligence Platform API...")


app = FastAPI(
    title="Business Listings Intelligence Platform API",
    description="Production-grade REST API for collecting, managing, filtering, and analyzing verified Indian business listings from OpenStreetMap.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware for React development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules under /api prefix
app.include_router(health.router, prefix="/api")
app.include_router(listings.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")


@app.get("/", include_in_schema=False)
def root():
    """Redirects base path to interactive Swagger documentation."""
    return RedirectResponse(url="/docs")


@app.get("/api", tags=["General"])
def api_root():
    """Returns general API platform metadata and endpoint discovery links."""
    return {
        "platform": "Business Listings Intelligence Platform",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/docs",
        "endpoints": {
            "health": "/api/health",
            "listings": "/api/listings",
            "bulk_insert": "/api/listings/bulk",
            "export_csv": "/api/listings/export",
            "summary": "/api/dashboard/summary",
            "city_wise": "/api/dashboard/city-wise",
            "category_wise": "/api/dashboard/category-wise",
            "source_wise": "/api/dashboard/source-wise",
            "data_quality": "/api/dashboard/data-quality"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
