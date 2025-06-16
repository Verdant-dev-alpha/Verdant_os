# basic create/read/update/delete functions
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

from .models import Pump, PumpActivity, PumpType, PumpAction

# ----- Pump CRUD operations -----

def get_pump(db: Session, pump_id: int) -> Optional[Pump]:
    """Get a pump by ID"""
    return db.query(Pump).filter(Pump.id == pump_id).first()

def get_pump_by_name(db: Session, name: str) -> Optional[Pump]:
    """Get a pump by name"""
    return db.query(Pump).filter(Pump.name == name).first()

def get_pumps(db: Session, skip: int = 0, limit: int = 100) -> List[Pump]:
    """Get all pumps with pagination"""
    return db.query(Pump).offset(skip).limit(limit).all()

def get_pumps_by_type(db: Session, pump_type: PumpType) -> List[Pump]:
    """Get all pumps of a specific type"""
    return db.query(Pump).filter(Pump.type == pump_type).all()

def create_pump(db: Session, name: str, pin: int, pump_type: PumpType, description: Optional[str] = None) -> Pump:
    """Create a new pump"""
    db_pump = Pump(
        name=name,
        pin=pin,
        type=pump_type,
        description=description,
        is_active=False
    )
    db.add(db_pump)
    db.commit()
    db.refresh(db_pump)
    return db_pump

def update_pump(db: Session, pump_id: int, data: Dict[str, Any]) -> Optional[Pump]:
    """Update a pump's details"""
    db_pump = get_pump(db, pump_id)
    if db_pump:
        for key, value in data.items():
            if hasattr(db_pump, key):
                setattr(db_pump, key, value)
        db.commit()
        db.refresh(db_pump)
    return db_pump

def delete_pump(db: Session, pump_id: int) -> bool:
    """Delete a pump"""
    db_pump = get_pump(db, pump_id)
    if db_pump:
        db.delete(db_pump)
        db.commit()
        return True
    return False

def set_pump_active(db: Session, pump_id: int, is_active: bool) -> Optional[Pump]:
    """Set a pump's active status"""
    db_pump = get_pump(db, pump_id)
    if db_pump:
        db_pump.is_active = is_active
        db_pump.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_pump)
    return db_pump

# ----- PumpActivity CRUD operations -----

def get_pump_activity(db: Session, activity_id: int) -> Optional[PumpActivity]:
    """Get a pump activity by ID"""
    return db.query(PumpActivity).filter(PumpActivity.id == activity_id).first()

def get_pump_activities(db: Session, skip: int = 0, limit: int = 100) -> List[PumpActivity]:
    """Get all pump activities with pagination"""
    return db.query(PumpActivity).order_by(PumpActivity.timestamp.desc()).offset(skip).limit(limit).all()

def get_pump_activities_by_pump(db: Session, pump_id: int, skip: int = 0, limit: int = 100) -> List[PumpActivity]:
    """Get activities for a specific pump"""
    return db.query(PumpActivity).filter(PumpActivity.pump_id == pump_id).order_by(PumpActivity.timestamp.desc()).offset(skip).limit(limit).all()

def create_pump_activity(db: Session, pump_id: int, action: PumpAction, duration: Optional[float] = None) -> PumpActivity:
    """Create a new pump activity record"""
    db_activity = PumpActivity(
        pump_id=pump_id,
        action=action,
        timestamp=datetime.utcnow(),
        duration=duration
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def update_pump_activity_duration(db: Session, activity_id: int, duration: float) -> Optional[PumpActivity]:
    """Update the duration of a pump activity (typically called when a pump is turned off)"""
    db_activity = get_pump_activity(db, activity_id)
    if db_activity:
        db_activity.duration = duration
        db.commit()
        db.refresh(db_activity)
    return db_activity

def delete_pump_activity(db: Session, activity_id: int) -> bool:
    """Delete a pump activity record"""
    db_activity = get_pump_activity(db, activity_id)
    if db_activity:
        db.delete(db_activity)
        db.commit()
        return True
    return False

# ----- Convenience functions -----

def record_pump_on(db: Session, pump_name: str) -> Dict[str, Any]:
    """Record that a pump has been turned on"""
    db_pump = get_pump_by_name(db, pump_name)
    if not db_pump:
        return {"success": False, "message": f"Pump '{pump_name}' not found"}

    # Set pump as active
    db_pump = set_pump_active(db, db_pump.id, True)

    # Create activity record
    activity = create_pump_activity(db, db_pump.id, PumpAction.ON)

    return {
        "success": True,
        "pump": db_pump.name,
        "action": "on",
        "timestamp": activity.timestamp
    }

def record_pump_off(db: Session, pump_name: str) -> Dict[str, Any]:
    """Record that a pump has been turned off"""
    db_pump = get_pump_by_name(db, pump_name)
    if not db_pump:
        return {"success": False, "message": f"Pump '{pump_name}' not found"}

    # Find the most recent ON activity for this pump
    last_on_activity = db.query(PumpActivity).filter(
        PumpActivity.pump_id == db_pump.id,
        PumpActivity.action == PumpAction.ON
    ).order_by(PumpActivity.timestamp.desc()).first()

    # Calculate duration if we have a previous ON activity
    duration = None
    if last_on_activity:
        now = datetime.utcnow()
        duration = (now - last_on_activity.timestamp).total_seconds()
        update_pump_activity_duration(db, last_on_activity.id, duration)

    # Set pump as inactive
    db_pump = set_pump_active(db, db_pump.id, False)

    # Create activity record
    activity = create_pump_activity(db, db_pump.id, PumpAction.OFF, duration)

    return {
        "success": True,
        "pump": db_pump.name,
        "action": "off",
        "duration": duration,
        "timestamp": activity.timestamp
    }

def initialize_pumps_from_config(db: Session, pump_config: Dict[str, int]) -> List[Pump]:
    """Initialize pumps in the database from a configuration dictionary"""
    pumps = []

    for name, pin in pump_config.items():
        # Determine pump type based on name
        if name.startswith(("flush", "fill")):
            pump_type = PumpType.HIGH_VOLUME
        else:
            pump_type = PumpType.NUTRIENT

        # Check if pump already exists
        existing_pump = get_pump_by_name(db, name)
        if existing_pump:
            # Update pin if it changed
            if existing_pump.pin != pin:
                update_pump(db, existing_pump.id, {"pin": pin})
            pumps.append(existing_pump)
        else:
            # Create new pump
            new_pump = create_pump(db, name, pin, pump_type)
            pumps.append(new_pump)

    return pumps
