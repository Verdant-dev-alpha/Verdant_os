# code that reads your DATABASE_URL and creates a Session/engine
import os
import logging
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from packages.secrets import get_secret, DB_USER_SECRET, DB_PASSWORD_SECRET, DB_NAME_SECRET

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database connection parameters
DB_USER = get_secret(DB_USER_SECRET, os.environ.get("db_username", "[username]"))  # Fetch from secret manager with fallback
DB_PASSWORD = get_secret(DB_PASSWORD_SECRET, os.environ.get("db_password", "[password]"))  # Fetch from secret manager with fallback
DB_NAME = get_secret(DB_NAME_SECRET, os.environ.get("db_name", "Byte-Algae"))  # Fetch from secret manager with fallback

# Check if running in Cloud environment with Cloud SQL
INSTANCE_CONNECTION_NAME = os.environ.get("INSTANCE_CONNECTION_NAME")
if INSTANCE_CONNECTION_NAME:
    logger.info(f"Using Cloud SQL Unix socket connection for {INSTANCE_CONNECTION_NAME}")
    # Format for Unix socket connection to Cloud SQL
    DB_HOST = f"/cloudsql/{INSTANCE_CONNECTION_NAME}"

    # URL-encode username and password to handle special characters
    encoded_user = urllib.parse.quote_plus(DB_USER)
    encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

    DATABASE_URL = f"postgresql+psycopg2://{encoded_user}:{encoded_password}@/{DB_NAME}?host={DB_HOST}"
else:
    # Standard TCP connection
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    logger.info(f"Using standard TCP connection to {DB_HOST}:{DB_PORT}")

    # URL-encode username and password to handle special characters
    encoded_user = urllib.parse.quote_plus(DB_USER)
    encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

    DATABASE_URL = os.environ.get(
        "DATABASE_URL", 
        f"postgresql+psycopg2://{encoded_user}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL
)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
