from src.custom.queue.redis_client import RedisQueue
from src.custom.workers.healthconnect_worker import HealthConnectWorker

redis_queue = RedisQueue()

opensearch_creds = {
    "schema_type": "http",
    "host": "localhost",
    "port": 9200,
    "verify_certs": False,
}

worker = HealthConnectWorker(
    redis_queue=redis_queue,
    opensearch_creds=opensearch_creds,
    batch_size=10,
)

worker.run_once()

print("worker run completed")
