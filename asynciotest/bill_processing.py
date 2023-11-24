import asyncio
import datetime
import random

from pymongo import MongoClient


class BillProcessing:
    def __init__(self, fname):
        self.fname = fname
        try:
            mongo = MongoClient("localhost:27017")
            self.db = mongo["temp"]
            self.col = self.db["bills"]
        except Exception as ex:
            print(ex)

    async def start_processing(self):
        # print("started processing")
        self.update_status_in_db(0, "Processing")
        asyncio.create_task(self.convert_pdf())

    async def convert_pdf(self):
        # print("started conversion")
        etime = await self.random_sleep(1, 10)
        self.update_status_in_db(etime, "Conversion")
        asyncio.create_task(self.upload_s3())

    async def upload_s3(self):
        # print("started s3upload")
        etime = await self.random_sleep(1, 20)
        self.update_status_in_db(etime, "S3Upload")
        asyncio.create_task(self.extract_ents())

    async def extract_ents(self):
        # print("started extraction")
        etime = await self.random_sleep(1, 50)
        self.update_status_in_db(etime, "Extraction")
        asyncio.create_task(self.save_bill())

    async def save_bill(self):
        # print("started savebill")
        etime = await self.random_sleep(1, 10)
        self.update_status_in_db(etime, "SaveBill")
        asyncio.create_task(self.completed())

    async def completed(self):
        # print("started savebill")
        etime = await self.random_sleep(1, 10)
        self.update_status_in_db(etime, "Completed")

    def update_status_in_db(self, etime, status):
        if status == "Completed":
            self.col.delete_one({"file_name": self.fname})
            return
        ts = datetime.datetime.now()
        petime = 0
        res = self.col.find_one({"file_name": self.fname}, {"etime": 1})
        if res != None:
            petime = int(res["etime"])
        self.col.update_one(
            {"file_name": self.fname},
            {"$set": {"status": status, "etime": petime + etime, "updated_at": ts}},
            upsert=True,
        )

    async def random_sleep(
        self, start, end
    ):  # simulate a task with random execution time
        sec = random.randint(start, end)
        await asyncio.sleep(sec)
        return sec
