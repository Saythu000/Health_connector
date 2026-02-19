from src.custom.queue.redis_client import RedisQueue
from datetime import datetime

queue = RedisQueue()

event = {
    "event_time": datetime.utcnow().isoformat(),
    "end_time": datetime.utcnow().isoformat(),
    "user_id": "user_001",
    "device_id": "pixel_8",
    "activity_id": "walk_001",
    "activity_type": "walking",
    "duration_seconds":600,
    "source": "healthconnect",
    "steps": 900,
    "calories_kcal": 55.5,
}

queue.push(event)

print(" Event pushed to Redis")