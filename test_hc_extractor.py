from src.custom.extractors.healthconnect import HealthConnectExtractor
from testschhc import sample_json  # reuse your validated sample

extractor = HealthConnectExtractor(sample_json)

for event in extractor():
    print(event)
