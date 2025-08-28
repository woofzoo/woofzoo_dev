"""
Main FastAPI application entry point.

This module creates and configures the FastAPI application with all
necessary middleware, routes, and startup/shutdown events.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.config import settings
from app.database import close_db, init_db
from app.routes import auth_router, owner_router, pet_router, pet_types_router, family_router, family_member_router, family_invitation_router, photo_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events for the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
    # Startup
    print("🚀 Starting WoofZoo API...")
    init_db()
    print("✅ Database initialized successfully")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down WoofZoo API...")
    close_db()
    print("✅ Database connections closed")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A modern FastAPI project following clean architecture principles",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    debug=settings.debug,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for security
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.debug else ["localhost", "127.0.0.1"]
)

# Include API routes
app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(owner_router, prefix=settings.api_prefix)
app.include_router(pet_router, prefix=settings.api_prefix)
app.include_router(pet_types_router, prefix=settings.api_prefix)
app.include_router(family_router, prefix=settings.api_prefix)
app.include_router(family_member_router, prefix=settings.api_prefix)
app.include_router(family_invitation_router, prefix=settings.api_prefix)
app.include_router(photo_router, prefix=settings.api_prefix)


@app.get("/", tags=["root"])
def root():
    """
    Root endpoint.
    
    Returns:
        Welcome message and API information
    """
    return {
        "message": f"Welcome to {settings.app_name} API!",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json"
    }


@app.get("/health", tags=["health"])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status information
    """
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )
