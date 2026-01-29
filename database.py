import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# 1. Direct fetch with cleaning
# We use os.environ.get directly to bypass any potential issues in config.py
raw_url = os.environ.get("DATABASE_URL", "")

def get_clean_url(url: str) -> str:
    if not url:
        return ""
    
    # Remove invisible characters like \r, \n, spaces, or quotes
    # This happens often when copy-pasting into Render
    clean_url = url.strip().replace('"', '').replace("'", "").replace('\r', '')
    
    # Standardize the prefix
    if clean_url.startswith("postgres://"):
        clean_url = clean_url.replace("postgres://", "postgresql://", 1)
        
    return clean_url

db_url = get_clean_url(raw_url)

# 2. Validation Check
if not db_url:
    print("❌ CRITICAL ERROR: DATABASE_URL is empty or not found in environment!")
else:
    # Log the host (masked) so you can see it in Render logs to confirm it's loaded
    try:
        masked_host = db_url.split("@")[1]
        print(f"✅ Database variable loaded. Target host: {masked_host}")
    except:
        print("❌ CRITICAL ERROR: DATABASE_URL exists but is malformed (missing '@')")

# 3. SQLAlchemy Setup
# We use a try/except here so the app gives a better error if it still fails
try:
    engine = create_engine(
        db_url,
        connect_args={"sslmode": "require"},
        poolclass=NullPool
    )
except Exception as e:
    print(f"❌ SQLAlchemy Engine Error: {e}")
    # We set a dummy engine to prevent the import from crashing the whole app immediately
    # though the app will fail when it tries to query.
    engine = None

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    if engine is None:
        raise Exception("Database engine was not initialized properly.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()