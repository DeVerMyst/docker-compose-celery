import os
import time

from celery import Celery

# Configuration dynamique via Docker Compose
BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

app = Celery("ml_tasks", broker=BROKER_URL, backend=RESULT_BACKEND)

@app.task(name="predict_task")
def predict_task():
    # Simulation d'un modèle d'IA lourd
    processing_time = int(os.getenv("MODEL_LATENCY", "5"))
    time.sleep(processing_time)
    return {"status": "complete", "prediction": 42} # La réponse de l'univers