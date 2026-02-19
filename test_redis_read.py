from src.custom.queue.redis_client import RedisQueue
queue = RedisQueue()
item = queue.pop()
print("POPPED ITEM FROM REDIS:")
print(item)

#HealthConnect JSON -> extractor(validated + flattened) -> Redis Queue (JSON-safe, FIFO) Nothing is indexed yet 