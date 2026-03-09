from celery.result import AsyncResult
from fastapi import FastAPI

from worker import predict_task

app = FastAPI()


@app.post("/predict")
def run_prediction():
    # On envoie la tâche au broker sans attendre
    job = predict_task.delay()
    return {"task_id": job.id}


@app.get("/status/{task_id}")
def get_status(task_id: str):
    # On vérifie l'état dans le Result Backend
    res = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": res.status,  # PENDING, STARTED, SUCCESS
        "result": res.result if res.ready() else None,
    }
