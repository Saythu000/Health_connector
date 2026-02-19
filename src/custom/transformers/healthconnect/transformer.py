import logging
from typing import Iterator, Dict, Any

from ..base import BaseTransformer
from .schemas import HealthEventDocument

logger = logging.getLogger(__name__)

class HealthConnectTransformer(BaseTransformer):
    """ 
    Transforms HealthConnect extracted events into index-ready documents.
    """
    
    def __init__(self, data, config: Dict[str, Any]):
        super().__init__(config)
        self.data = data
        
        
    def __call__(self) -> Iterator[Dict[str, Any]]:
        """ 
        Generator of Elasticsearch/Opensearch documents
        """
        
        for raw in self.data:
            try:
                event = HealthEventDocument(**raw)
                
                record = event.model_dump(mode="json")
                
                # required for time-series & ISM
                record["@timestamp"] = record["event_time"]
                
                doc_id = f"{record['user_id']}|{record['activity_id']}|{record['event_time']}"
                
                yield {"_index": self.index_name,
                       "_id": doc_id,
                       "_source": record}
                
                #yield self.transform(record)
                
            except Exception as e:
                logger.error(f"HealthConnect transform failed: {e}")
                continue