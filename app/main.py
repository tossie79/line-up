from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.endpoints import users


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="A simple API to fetch user data from reqres.in",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(users.router, prefix="/api/v1", tags=["users"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.PROJECT_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        content={"status": "healthy", "service": settings.PROJECT_NAME}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=settings.DEBUG
    )