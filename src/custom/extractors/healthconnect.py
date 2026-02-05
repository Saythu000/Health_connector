import logging
from typing import Dict, Any, Iterator

from .base import BaseExtractor
from .schemas.healthconnector import HealthConnectPayload

logger = logging.getLogger(__name__)

class HealthConnectExtractor(BaseExtractor):
    """
    Purpose:
       Converts HealthConnectPayload into flat,
       time-series-ready activity records.
    """
    
    def __init__(self, payload: Dict[str, Any]):
        """
        Args:
            payload (dict): Raw Health Connect JSON payload
        """
        
        #Validate once at the boundary
        self.payload = HealthConnectPayload(**payload)
        
        logger.info(
            "HealthConnectorExtractor initialized | user=%s activities=%d",
            self.payload.user.get("user_id"),
            len(self.payload.activities),
        )
        
    
    def __call__(self) -> Iterator[Dict[str, Any]]:
        return self.extract()
    
    
    def extract(self) -> Iterator[Dict[str, Any]]:
        """ 
        Yields one record per activity (time-series event)
        """
        
        user_id = self.payload.user.get("user_id")
        device_id = self.payload.device.get("device_id")
        
        for activity in self.payload.activities:
           
            record = {
                "event_time": activity.start_time,
                "end_time": activity.end_time,
                "user_id": user_id,
                "device_id": device_id,
                "activity_id": activity.activity_id,
                "activity_type": activity.activity_type,
                "duration_seconds": activity.duration_seconds,
                "source": self.payload.source,
            }
            
            
            
            #Flatten metrics safely
            metrics = activity.metrics
            if metrics:
                #print("DEBUG metrics:", metrics)
                #print("DEBUG calories:", metrics.calories_kcal)
                record.update({
                    "steps": metrics.steps,
                    "distance_meters": metrics.distance_meters,
                    "calories_kcal": metrics.calories_kcal,
                    "avg_hr_bpm": metrics.average_heart_rate_bpm,
                    "max_hr_bpm": metrics.max_heart_rate_bpm,
                    "elevation_gain_m":metrics.elevation_gain_meters,
                    "active_zone_minutes": metrics.active_zone_minutes,
                    
                })
                
            yield record

       