from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import router as metrics_router
from database import engine, Base
from config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DaySense AI Backend",
    description="Production-ready backend for DaySense AI mobile application",
    version="2.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust to production origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(metrics_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "DaySense AI API is running",
        "version": "2.0.0",
        "environment": settings.ENVIRONMENT
    }
