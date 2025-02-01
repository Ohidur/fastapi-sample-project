from celery import Celery
import time
import pymongo
from os import environ as env

celery_app = Celery(
    "worker",
    broker=f"redis://redis:{env['REDIS_PORT']}/0",
    backend=f"mongodb://{env['MONGO_INITDB_ROOT_USERNAME']}:{env['MONGO_INITDB_ROOT_PASSWORD']}@mongodb:{env['MONGO_PORT']}/tasks?authSource=admin"
)

# print("Env: ", env['MONGO_INITDB_ROOT_USERNAME'])
# MongoDB client
# client = pymongo.MongoClient("mongodb://mongodb:27017/")
client = pymongo.MongoClient(f"mongodb://{env['MONGO_INITDB_ROOT_USERNAME']}:{env['MONGO_INITDB_ROOT_PASSWORD']}@mongodb:{env['MONGO_PORT']}/?authSource=admin")
db = client["celery_db"]
collection = db["task_results"]

@celery_app.task
def create_task(data):
    time.sleep(5)  # Simulate a long-running task
    result = {"data": data, "status": "completed"}
    collection.insert_one(result)
    return result


