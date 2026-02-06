from src.custom.connectors.opensearch import OpensearchConnector
from src.custom.loaders.factory import LoaderFactory
from src.custom.transformers.healthconnect.transformer import HealthConnectTransformer

# 1️ Sample transformed record (THIS is what loader expects)
raw_events = [
    {
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
]


# Run transformer
transformer = HealthConnectTransformer(
    data=raw_events,
    config={"index_name": "healthconnect-events-write"}
) 

transformed_records = list(transformer())

print("TRANSFORMED RECORD COUNT:", len(transformed_records))
print("SAMPLE RECORD:", transformed_records[0])

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

#records = list(transformed_records)

#print("TRANSFORMED RECORD COUNT:", len(records))
#print("SAMPLE RECORD:", records[0] if records else "NO DATA")


# 5️ Load data
loader(transformed_records)

print("✅ Load function executed")
