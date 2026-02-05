from src.custom.connectors.opensearch import OpensearchConnector
from src.custom.loaders.factory import LoaderFactory

# 1️ Sample transformed record (THIS is what loader expects)
transformed_records = [
    {
        "_index": "healthconnect-events",
        "_source": {
            "event_time": "2024-10-01T10:05:00+00:00",
            "end_time": "2024-10-01T10:45:00+00:00",
            "user_id": "user_001",
            "device_id": "pixel_8",
            "activity_id": "act_001",
            "activity_type": "walking",
            "duration_seconds": 2400,
            "source": "healthconnect",
            "steps": 3200,
            "calories_kcal": 120.5
        }
    }
]

# 2️ OpenSearch credentials (local)
opensearch_creds = {
    "schema_type": "http",
    "host": "localhost",
    "port": 9200,
    "verify_certs": False
}

# 3️ Connect to OpenSearch
client = OpensearchConnector(opensearch_creds)()

# 4️ Create loader
loader = LoaderFactory.get_loader(
    "opensearch",
    connection=client,
    config={
        "index_name": "healthconnect-events-write",
        "settings": {},
        "mappings": {}
    }
)

# 5️ Load data
loader(transformed_records)

print("✅ HealthConnect data indexed successfully")
