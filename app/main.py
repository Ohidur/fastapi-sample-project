from fastapi import FastAPI
from tasks import create_task
from pymongo import MongoClient
from os import environ as env

client = MongoClient(f"mongodb://{env['MONGO_INITDB_ROOT_USERNAME']}:{env['MONGO_INITDB_ROOT_PASSWORD']}@mongodb:{env['MONGO_PORT']}/?authSource=admin")
db = client["celery_db"]
collection = db["task_results"]

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI with Celery and Docker Compose"}

@app.post("/tasks/{data}")
def run_task(data: str):
    task = create_task.delay(data)
    return {"task_id": task.id, "status": "Processing"}

@app.get("/tasks/")
def get_all_tasks():
    tasks = list(collection.find({}, {"_id": 0}))
    return {"tasks": tasks}




