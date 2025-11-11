import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

# load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
# POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# SQLALCHEMY_DATABASE_URL = "postgresql://root:password@postgres-service:5432/fastapi"

SQLALCHEMY_DATABASE_URL = (f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def wait_for_db(max_retries: int = 5, delay_seconds: int = 2):
    
    for attempt in range(1, max_retries + 1):
        try:
            
            with engine.connect() as conn:
                print("Database connection successful!")
                return
        except Exception as e:
            print(f"DB connection failed (Attempt {attempt}/{max_retries})")
            print(f"Error: {e}")
            
            if attempt < max_retries:
                time.sleep(delay_seconds)
            else:
                raise Exception("Database not available.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

