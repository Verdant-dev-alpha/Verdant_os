# Initialize the database package
from .connection import Base, engine, SessionLocal, get_db
from .models import Pump, PumpActivity, PumpType, PumpAction
from . import crud

def create_tables():
    """Create all tables in the database if they don't exist."""
    Base.metadata.create_all(bind=engine)

# Export commonly used components
__all__ = [
    "Base", "engine", "SessionLocal", "get_db",
    "Pump", "PumpActivity", "PumpType", "PumpAction",
    "crud", "create_tables"
]
