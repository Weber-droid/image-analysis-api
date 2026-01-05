import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import upload, analyze
from app.utils.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)
app = FastAPI(
    title="Image Analysis API",
    description="Backend service for mobile image analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, tags=["Upload"])
app.include_router(analyze.router, tags=["Analysis"])


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Image Analysis API is running"}


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "image-analysis-api",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Image Analysis API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)