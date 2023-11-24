import random
import time
from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = "redis://localhost:6379"
celery.conf.result_backend = "redis://localhost:6379"


@celery.task(name="celery_task")
def create_task(start, end):
    sec = random.randint(start, end)
    print(f"sleeping {sec} seconds")
    time.sleep(sec)
    return sec
