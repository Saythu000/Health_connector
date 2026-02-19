from src.custom.queue.redis_client import RedisQueue

queue = RedisQueue()

items = queue.pop_batch(10)

print("Pulled from Redis:", items)