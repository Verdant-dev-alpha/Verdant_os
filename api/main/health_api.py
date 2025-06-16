# Health API for cloud deployment
from fastapi import FastAPI
import logging
import os
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Verdant API Health Service")

@app.get("/health")
async def health_check():
    """Health check endpoint for cloud monitoring."""
    return {"status": "healthy", "service": "verdant-api"}

@app.get("/")
async def root():
    """Root endpoint that redirects to health check."""
    return {"message": "Verdant API is running. Use /health for health checks."}

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8000))
    
    # Log startup information
    logger.info(f"Starting Verdant API Health Service on port {port}")
    
    # Run the API with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)