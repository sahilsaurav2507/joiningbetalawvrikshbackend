"""
Main FastAPI application for LawVriksh Backend API.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import time
import logging
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db
from app.routes import auth, user
from app.utils.helpers import format_datetime

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting LawVriksh Backend API...")
    try:
        # Initialize database
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down LawVriksh Backend API...")


# Create FastAPI application
app = FastAPI(
    title="LawVriksh Backend API",
    description="Backend API for LawVriksh website - managing waiting lists, feedback, and admin operations",
    version="1.0.0",
    docs_url="/api/docs" if settings.debug else None,
    redoc_url="/api/redoc" if settings.debug else None,
    openapi_url="/api/openapi.json" if settings.debug else None,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add trusted host middleware for production
if not settings.debug:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["lawvriksh.com", "www.lawvriksh.com", "api.lawvriksh.com"]
    )


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url.path} - Client: {request.client.host if request.client else 'unknown'}")
    
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - Time: {process_time:.3f}s")
    
    return response


# Global exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "timestamp": format_datetime(time.time()),
            "path": request.url.path
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation exceptions."""
    logger.error(f"Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Validation error",
            "detail": exc.errors(),
            "timestamp": format_datetime(time.time()),
            "path": request.url.path
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "timestamp": format_datetime(time.time()),
            "path": request.url.path
        }
    )


# Health check endpoint
@app.get("/api/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": format_datetime(time.time()),
        "version": "1.0.0",
        "environment": settings.environment
    }


# Root endpoint
@app.get("/api/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to LawVriksh Backend API",
        "version": "1.0.0",
        "docs": "/api/docs" if settings.debug else "Not available in production",
        "health": "/api/health"
    }


# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])

# Include other routers if they exist
try:
    from app.routes import creator
    app.include_router(creator.router, prefix="/api/v1/creators", tags=["Creators"])
except ImportError:
    pass

try:
    from app.routes import feedback
    app.include_router(feedback.router, prefix="/api/v1/feedback", tags=["Feedback"])
except ImportError:
    pass

try:
    from app.routes import admin
    app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
except ImportError:
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    ) 