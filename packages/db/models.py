# SQLAlchemy models
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from .connection import Base

# Enum for pump types
class PumpType(enum.Enum):
    NUTRIENT = "nutrient"
    HIGH_VOLUME = "high_volume"

# Enum for pump actions
class PumpAction(enum.Enum):
    ON = "on"
    OFF = "off"

class Pump(Base):
    __tablename__ = "pumps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    pin = Column(Integer, unique=True)
    type = Column(Enum(PumpType))
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to PumpActivity
    activities = relationship("PumpActivity", back_populates="pump")

class PumpActivity(Base):
    __tablename__ = "pump_activities"

    id = Column(Integer, primary_key=True, index=True)
    pump_id = Column(Integer, ForeignKey("pumps.id"))
    action = Column(Enum(PumpAction))
    timestamp = Column(DateTime, default=datetime.utcnow)
    duration = Column(Float, nullable=True)  # Duration in seconds, if applicable

    # Relationship to Pump
    pump = relationship("Pump", back_populates="activities")
