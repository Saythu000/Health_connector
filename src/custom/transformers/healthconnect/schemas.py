from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

STRICT  =  ConfigDict(extra="forbid")

class HealthEventDocument(BaseModel):
    """
    Canonical Health Event stored in Opensearch
    """
    
    model_config = STRICT
    
    #--- Time ---
    event_time: datetime
    end_time:Optional[datetime] = None
    
    # --- Identity ---
    user_id: str
    device_id: str
    activity_id: str
    
    # --- Activity ---
    activity_type: str
    duration_seconds: int
    source: str = "healthconnect"
    
    # --- Metrics (nullable by design) ---
    steps: Optional[int] = None
    distance_meters: Optional[float] = None
    calories_kcal: Optional[float] = None
    avg_hr_bpm: Optional[int] = None
    max_hr_bpm: Optional[int] = None
    elevation_gain_m: Optional[float] = None
    active_zone_minutes: Optional[int] = None
    
        