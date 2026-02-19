from src.custom.workers.healthconnect_worker import HealthConnectWorker

worker = HealthConnectWorker()
worker.run_once()

print("WORKER RUN COMPLETED")