from src.custom.extractors.healthconnect import HealthConnectExtractor
from src.custom.queue.redis_client import RedisQueue

# 1️⃣ Sample HealthConnect payload (minimal)
payload = {
    "contract_version": "1.0",
    "source": "healthconnect",
    "user": {"user_id": "user_001"},
    "device": {"device_id": "pixel_8"},
    "sync_window": {
        "from": "2024-10-01T10:00:00Z",
        "to": "2024-10-01T11:00:00Z"
    },
    "activities": [
        {
            "activity_id": "act_001",
            "activity_type": "walking",
            "start_time": "2024-10-01T10:05:00Z",
            "end_time": "2024-10-01T10:45:00Z",
            "duration_seconds": 2400,
            "metrics": {
                "steps": 3200,
                "calories_kcal": 120.5
            },
            "source_metadata": {
                "app": "healthconnect",
                "device": "pixel_8"
            }
        }
    ]
}

# 2️⃣ Create Redis queue
redis_queue = RedisQueue()

# 3️⃣ Run extractor
extractor = HealthConnectExtractor(
    payload=payload,
    redis_queue=redis_queue
)

extractor()

print("✅ Events pushed to Redis")
