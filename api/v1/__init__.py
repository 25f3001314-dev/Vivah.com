# -*- coding: utf-8 -*-
"""
FastAPI Application
Vedic Matchmaking API - Ashtakoot Milan Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Import routers
from .routers import router as matchmaking_router
from .routers.by_name import router as match_by_name_router
from .routers.ashtakoot_match import router as ashtakoot_match_router

# Create FastAPI app
app = FastAPI(
    title="Vedic Matchmaking API",
    description="Backend API for Ashtakoot Milan (8-Koot) compatibility matching based on Vedic Astrology",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health():
    """Basic health check endpoint."""
    return {"status": "ok", "service": "vedic-matchmaking-api"}


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Vedic Matchmaking API",
        "version": "1.0.0",
        "description": "Backend for Ashtakoot Milan compatibility matching",
        "docs": "/api/docs",
        "endpoints": {
            "matchmaking": "/api/v1/matchmaking",
            "health": "/health",
        },
    }


# Include routers
app.include_router(matchmaking_router, prefix="/api/v1")
app.include_router(match_by_name_router, prefix="/api")
app.include_router(ashtakoot_match_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Vedic Matchmaking API server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
