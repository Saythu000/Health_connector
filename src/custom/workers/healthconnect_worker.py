import time
import logging
#from datetime import datetime
from typing import List
from collections import Counter

from src.custom.queue.redis_client import RedisQueue
from src.custom.transformers.healthconnect.transformer import HealthConnectTransformer
from src.custom.connectors.opensearch import OpensearchConnector
from src.custom.loaders.factory import LoaderFactory

logger = logging.getLogger(__name__)

class HealthConnectWorker:
    """
    Background worker that consumes HealthConnect events from Redis
    and indexes them into OpenSearch.
    """
    
    def __init__(
        self,
        redis_queue: RedisQueue,
        opensearch_creds: dict,
        batch_size: int = 50,
        ):
        
        self.redis_queue = redis_queue
        self.batch_size = batch_size
        
        self.metrics = Counter()
        #Opensearch client
        self.client = OpensearchConnector(opensearch_creds)()
        
        #Loader uses WRITE ALIAS
        self.loader = LoaderFactory.get_loader(
            "opensearch",
            connection=self.client,
            config={
                "index_name": "healthconnect-events-write",
                "settings": {},
                "mappings":{}
            }
        )
        
    def run_once(self):
        """ 
        Process a sngle batch from Redis.
        """
        raw_events= self.redis_queue.pop_batch(self.batch_size)
        if raw_events:
            print("DEBUG raw_events:", raw_events)
        if not raw_events:
            logger.info("No events in Redis queue")
            return
        
        self.metrics["pulled"] += len(raw_events)
        #logger.info("Pulled %d events from Redis", len(raw_events))
        
        #transformer
        transformer = HealthConnectTransformer(
            data=raw_events,
            config={"index_name": "healthconnect-events-write"}
        )
        
        documents = list(transformer())
        print("DEBUG documents:", documents)
        #count transformed
        self.metrics["transformed"] += len(documents)
        
        if not documents:
            self.metrics["failed"] += len(raw_events)
            logger.warning("All events failed transform")
            return
        
        MAX_RETRIES = 2
        
        
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                self.loader(documents)
                #Metrics: indexed
                self.metrics["indexed"] += len(documents)
                
                logger.info(
                    "Indexed %d documents into OpenSearch",
                    len(documents)
                )
                return
            
            except Exception as e:
                logger.error(
                    "Indexing attempt %d failed: %s",
                    attempt,
                    e
                )
                time.sleep(2)
                
        logger.error("All retries failed.sending events to DLQ")
        
        for record in raw_events:
            self.redis_queue.push_failed(record)
            self.metrics["dlq"] += 1  
            
        #retry → index → log success
        #no infinite loop
        #safe failure handling
        
        #replaced unsafe direct indexing + infinite loop with controlled retries and safe failure handling.
        
    def run_forever(self, sleep_seconds: int = 5):
        """ Continuously run the worker with a sleep interval. """
        logger.info("HealthConnect worker started.")
        
        try:
            while True:
                try:
                   self.run_once()
                   time.sleep(sleep_seconds)
                except Exception as e:
                    logger.exception("Workeriteration failed: %s", e)
                    time.sleep(5)
                    
        except KeyboardInterrupt:
            logger.info("Worker shutdown requested. Exiting gracefully.")
            logger.info("Final Metrics: %s", dict(self.metrics))