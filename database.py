import os
from sqlalchemy import create_engine, make_url
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# 1. Get the raw URL
raw_url = os.environ.get("DATABASE_URL", "").strip()

def create_safe_engine():
    try:
        if not raw_url:
            raise ValueError("DATABASE_URL is missing")

        # Clean the string of quotes or hidden characters
        clean_url = raw_url.replace('"', '').replace("'", "").replace('\r', '').strip()
        
        # Fix the prefix
        if clean_url.startswith("postgres://"):
            clean_url = clean_url.replace("postgres://", "postgresql://", 1)

        # DEBUG: Log the host to verify the variable is present
        print(f"✅ Attempting connection to: {clean_url.split('@')[-1]}")

        # MANUALLY parse the URL to bypass the faulty string parser
        url_obj = make_url(clean_url)

        return create_engine(
            url_obj,
            connect_args={"sslmode": "require"},
            poolclass=NullPool
        )
    except Exception as e:
        print(f"❌ CRITICAL ENGINE FAILURE: {e}")
        return None

# Initialize
engine = create_safe_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    if engine is None:
        print("❌ get_db called but engine is None")
        return
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()