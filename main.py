from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import router as metrics_router
from database import engine, Base
from config import settings

# Create database tables with safety wrap
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables verified/created successfully.")
except Exception as e:
    print(f"Database connection failed: {e}")
    # In production, you might not want to crash here, 
    # but the error will now be visible in Render logs.

app = FastAPI(
    title="DaySense AI Backend",
    description="Production-ready backend for DaySense AI mobile application",
    version="2.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(metrics_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "DaySense AI API is running",
        "version": "2.0.0",
        "environment": settings.ENVIRONMENT
    }