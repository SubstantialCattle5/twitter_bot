from typing import Union

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.controllers.TwitterScrapperController import get_trends_data, run_trends_script

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/views/static"), name="static")
templates = Jinja2Templates(directory="src/views/templates")



@app.get("/", response_class=HTMLResponse)
async def home(req:Request):
    data = await get_trends_data()
    return templates.TemplateResponse("index.html", {"request": req, "data": data})    

@app.get("/run")
async def run_script():
    return await run_trends_script()