from datetime import datetime, timezone

from src.custom.transformers.healthconnect.transformer import HealthConnectTransformer

# -----------------------------
# Sample extractor output
# -----------------------------
sample_events = [
    {
        "event_time": datetime(2024, 10, 1, 10, 5, tzinfo=timezone.utc),
        "end_time": datetime(2024, 10, 1, 10, 45, tzinfo=timezone.utc),
        "user_id": "user_001",
        "device_id": "pixel_8",
        "activity_id": "act_001",
        "activity_type": "walking",
        "duration_seconds": 2400,
        "source": "healthconnect",
        "steps": 3200,
        "distance_meters": None,
        "calories_kcal": 120.5,
        "avg_hr_bpm": None,
        "max_hr_bpm": None,
        "elevation_gain_m": None,
        "active_zone_minutes": None,
    }
]

# -----------------------------
# Transformer config
# -----------------------------
config = {
    "index_name": "healthconnect-events-write"
}

# -----------------------------
# Run transformer
# -----------------------------
transformer = HealthConnectTransformer(sample_events, config)

for doc in transformer():
    print(doc)
