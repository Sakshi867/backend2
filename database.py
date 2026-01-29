import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from config import settings

# 1. Get the URL from settings
db_url = settings.DATABASE_URL

if not db_url:
    raise ValueError("DATABASE_URL is not set in environment variables.")

# 2. Standardize protocol (Supabase uses postgres://, SQLAlchemy needs postgresql://)
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# 3. Configure for Transaction Pooler (Port 6543)
# We remove 'check_same_thread' because it crashes Postgres connections.
if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    engine = create_engine(db_url, connect_args=connect_args)
else:
    # Settings for Supabase Transaction Pooler
    connect_args = {
        "prepare_threshold": None,  # Required for Transaction Mode
        "sslmode": "require"
    }
    engine = create_engine(
        db_url, 
        connect_args=connect_args,
        poolclass=NullPool  # Prevents connection accumulation
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()