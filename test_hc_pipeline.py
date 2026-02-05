# 1. Extract
payload = HealthConnectPayload(**sample_json)
extractor = HealthConnectExtractor(payload)
events = extractor()

# 2. Transform
transformer = HealthConnectTransformer(events, {
    "index_name": "healthconnect-events"
})
records = list(transformer())

# 3. Load
client = OpensearchConnector(creds)()
loader = LoaderFactory.get_loader(
    "opensearch",
    connection=client,
    config=opensearch_config
)

loader(records)
