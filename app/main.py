from fastapi import FastAPI
from app.api.endpoints import metrics
from app.db.database import engine, Base
from app.core.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DaySense AI Backend",
    description="Production-ready backend for DaySense AI mobile application",
    version="1.0.0"
)

# Include routers
app.include_router(metrics.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "DaySense AI API is running", "environment": settings.ENVIRONMENT}
