from src.custom.queue.redis_client import RedisQueue
from src.custom.workers.healthconnect_worker import HealthConnectWorker

redis_queue = RedisQueue()

opensearch_creds = {
    "schema_type": "http",
    "host": "localhost",
    "port": 9200,
    "verfy_certs": False
}

worker = HealthConnectWorker(redis_queue, opensearch_creds)

worker.run_forever()