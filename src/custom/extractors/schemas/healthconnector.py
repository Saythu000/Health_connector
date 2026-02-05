from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional, Literal
from datetime import datetime

#---------------------
# Activity Metrics
#---------------------

class ActivityMetrics(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    
    steps: Optional[int] = None
    distance_meters: Optional[float] = None
    calories_kcal: Optional[float] = None
    average_heart_rate_bpm: Optional[int] = None
    max_heart_rate_bpm: Optional[int] = None
    elevation_gain_meters: Optional[float] = None
    active_zone_minutes: Optional[int] = None
    
    
    
#---------------------
#Activity Record
#---------------------

class HealthActivity(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    
    activity_id: str
    activity_type: str
    
    start_time: datetime
    end_time: datetime
    duration_seconds: int
    
    
    metrics: ActivityMetrics
    
    source_metadata: Dict[str, str]
    
    
#-----------------------
#sync Window
#-----------------------

class SyncWindow(BaseModel):
    from_time: datetime = Field(alias="from")
    to_time: datetime = Field(alias="to")
    
    

#----------------------
#Root Payload Contract
#----------------------

class HealthConnectPayload(BaseModel):
    """
    This is the Main contract Health Connect must send.
    """
    
    model_config = ConfigDict(extra="forbid")
    
    
    contract_version: str
    source: str = "healthconnector"
    #syn_type: Literal["hourly", "daily"]
    
    
    user: Dict[str, str]
    device: Dict[str, str]
    
    
    sync_window : SyncWindow
    activities: List[HealthActivity]
    
    