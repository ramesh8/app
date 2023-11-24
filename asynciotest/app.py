from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pymongo import MongoClient
import pymongo
from bill_processing import BillProcessing
import asyncio
from fastapi.templating import Jinja2Templates

app = FastAPI()
mongo = None
db = None
col = None
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def startup():
    try:
        global mongo, db, col
        mongo = MongoClient("localhost:27017")
        db = mongo["temp"]
        col = db["bills"]
    except Exception as ex:
        raise HTTPException(status_code=501, detail="Unable to start db server")
    pass


@app.get("/tasks/", response_class=JSONResponse)
def get_tasks():
    tasks = list(
        col.find({"status": {"$ne": "Completed"}}, {"_id": 0}).sort(
            "file_name", pymongo.ASCENDING
        )
    )
    for task in tasks:
        task["updated_at"] = str(task["updated_at"])
    return JSONResponse(tasks)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.get("/post_bill", response_class=JSONResponse)
async def post_bill(
    request: Request, bill_file: str, background_tasks: BackgroundTasks
):
    print(f"processing {bill_file}")
    bp = BillProcessing(bill_file)
    background_tasks.add_task(bp.start_processing)
    # bp.start_processing()
    return JSONResponse({"message": f"bill processing started for {bill_file}"})
