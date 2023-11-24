import asyncio
import datetime
import json
import random

from pymongo import MongoClient
from celery.result import AsyncResult
from worker import create_task


class BillProcessing:
    def __init__(self, fname):
        self.fname = fname
        try:
            mongo = MongoClient("localhost:27017")
            self.db = mongo["temp"]
            self.col = self.db["bills"]
        except Exception as ex:
            print(ex)

    def start_processing(self):
        task = create_task.delay(1, 10)
        task_result = AsyncResult(task.id)
        self.update_status_in_db(task_result, "Processing")
        self.convert_pdf()

    def convert_pdf(self):
        task = create_task.delay(1, 30)
        task_result = AsyncResult(task.id)
        self.update_status_in_db(task_result, "Conversion")
        self.upload_s3()

    def upload_s3(self):
        task = create_task.delay(1, 30)
        task_result = AsyncResult(task.id)
        self.update_status_in_db(task_result, "S3Upload")
        self.extract_ents()

    def extract_ents(self):
        task = create_task.delay(10, 50)
        task_result = AsyncResult(task.id)
        self.update_status_in_db(task_result, "Extraction")
        self.save_bill()

    def save_bill(self):
        task = create_task.delay(1, 10)
        task_result = AsyncResult(task.id)
        self.update_status_in_db(task_result, "SaveBill")
        self.finish_bill()

    def finish_bill(self):
        task = create_task.delay(1, 10)
        task_result = AsyncResult(task.id)
        self.update_status_in_db(task_result, "Completed")

    def update_status_in_db(self, taskres, label):
        ts = datetime.datetime.now()
        petime = 0
        res = self.col.find_one({"file_name": self.fname}, {"etime": 1})
        if res == None:
            petime = 0
        elif "etime" in res:
            petime = int(res["etime"])
        # print(taskres, "🍷")
        # result = taskres.get()
        # print(result)
        self.col.update_one(
            {"file_name": self.fname},
            {
                "$set": {
                    "task": {
                        "status": taskres.status,
                        "id": taskres.id,
                        # "result": result,
                    },
                    "status": label,
                    # "etime": petime + int(result),
                    "updated_at": ts,
                }
            },
            upsert=True,
        )
