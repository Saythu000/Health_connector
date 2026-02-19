# import json
# import logging
# from typing import Optional

# import redis

# logger = logging.getLogger(__name__)

# class RedisQueue:
#     """
#     Simple Redis-based FIFO queue for HealthConnector events.
#     """
    
#     def __init__(
#         self,
#         host: str = "localhost",
#         port: int = 6379,
#         db: int  = 0,
#         queue_name: str = "healthconnect:events",
#     ):
#         """
#         Initialize Redis connection and queue name.
#         Args:
#             host (str, optional): _description_. Defaults to "localhost".
#             port (int, optional): _description_. Defaults to 6379.
#             db (int, optional): _description_. Defaults to 0.
#             queue_name (_type_, optional): _description_. Defaults to "healthconnect:events".
#         """
        
#         self.queue_name = queue_name
#         # Creat Redis client
#         self.client = redis.Redis(
#             host=host,
#             port=port,
#             db=db,
#             decode_responses=True, # return strings, not bytes
#         )
        
#         #Test connection early
#         try:
#             self.client.ping()
#             logger.info("Connected to Redis successfully")
#         except redis.ConnectionError as e:
#             logger.error("Could not connect to Redis")
#             raise e
        
#     def push(self, item:dict) -> None: # -> add event to queue
#         """ Push one event into Redis queue (Right side)
#         Args:
#             item (dict): Event data to be pushed into the queue
#         """
        
#         payload = json.dumps(item) #Convert Python dict -> JSON string
#         self.client.rpush(self.queue_name, payload)
#         #Add to Right of Redis list First in -. first out
#     def pop(self) -> Optional[dict]: # read event from queue
#         """ Pop one event from Redis queue (Left side)
#         Returns:
#             Optional[dict]: Event data popped from the queue, or None if queue is empty
#         """
        
#         payload = self.client.lpop(self.queue_name) #Remove from LEFT , Oldest event comes out first
#         if payload is None:
#             return None
        
#         return json.loads(payload) #JSON -> Pyhton dict
        
#     def size(self) -> int: #queue length
#         """
#         Return Current Queue length.
#         Returns:
#             int: _description_
#         """
        
#         return self.client.llen(self.queue_name)
        
#         #Extractor → Redis -> Worker → Transformer → OpenSearch


import json
import redis
from datetime import datetime
from typing import Any, Dict, List


class RedisQueue:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        queue_name: str = "healthconnect:events",
    ):
        self.queue_name = queue_name
        self.failed_queue_name = f"{queue_name}:failed"
        
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,  # IMPORTANT for JSON
        )

    def _serialize(self, obj: Any):
        """
        Recursively convert non-JSON types into JSON-safe values
        """
        if isinstance(obj, datetime):
            return obj.isoformat()

        if isinstance(obj, dict):
            return {k: self._serialize(v) for k, v in obj.items()}

        if isinstance(obj, list):
            return [self._serialize(v) for v in obj]

        return obj

    def push(self, item: Dict[str, Any]):
        #Push item to main queue (FIFO)
        safe_item = self._serialize(item)
        payload = json.dumps(safe_item)
        self.client.lpush(self.queue_name, payload)

    def pop(self) -> Dict[str, Any] | None:
        #Pop single item from queue(FIFO)
        raw = self.client.rpop(self.queue_name)
        if raw:
             return None
        return json.loads(raw)
       

    def pop_batch(self, batch_size: int) -> List[Dict[str, Any]]:
        """
        Pop up to batch_size items from Redis queue(FIFO).
        """
        items = []
        
        for _ in range(batch_size):
            raw = self.client.rpop(self.queue_name)
            if raw is None:
                break
            
            items.append(json.loads(raw))
            
        return items
    
    
    def push_failed(self, item:Dict[str, Any]):
        safe_item = self._serialize(item)
        payload = json.dumps(safe_item)
        self.client.lpush(self.failed_queue_name,payload)