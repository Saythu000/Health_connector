from src.custom.queue.redis_client import RedisQueue

# Create queue client
queue = RedisQueue()

print("---- PUSH TEST ----")
queue.push({"test": "ok"})
print("Pushed {'test': 'ok'}")

print("\n---- BATCH POP TEST ----")
items = queue.pop_batch(10)
print("Popped items:", items)

print("\n---- DLQ TEST ----")
queue.push_failed({"error": "test"})
print("Pushed {'error': 'test'} to DLQ")
