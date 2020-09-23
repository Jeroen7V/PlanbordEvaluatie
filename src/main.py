from typing import List
import os
import csv
from os.path import isfile, join
from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from . import models, schemas
from .database import SessionLocal, engine

if "src" in os.listdir(os.getcwd()):
    #os.chown("src", os.getuid(), os.getgid())
    os.chdir("src")

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

#127.0.0.1:8000?p_symbol=aardbei&p_task=kuisen&p_difficult=1&p_like=0
@app.get("/", include_in_schema=False)
def get_html(
    request: Request, db: Session = Depends(get_db), p_symbol: str = None, p_task: str = None, p_difficult: int = None, p_like: int = None
):

    if p_symbol:
        p_symbol = os.path.splitext(p_symbol)[0]
    if p_task:
        p_task = os.path.splitext(p_task)[0]

    if p_symbol and p_task and p_difficult is not None and p_like is not None:
        result = models.Result(
            date = datetime.now(),
            symbol=p_symbol,
            task=p_task,
            difficult=p_difficult,
            like=p_like,
        )
        db.add(result)
        db.commit()
        db.close()
        return RedirectResponse(
            "/"
        )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "symbols": os.listdir("static/images/symbols"),
            "tasks": os.listdir("static/images/tasks"),
            "p_symbol": p_symbol,
            "p_task": p_task,
            "p_difficult": p_difficult,
            "p_like": p_like,
        },
    )

# Geschreven door Yoni
@app.get("/overview", include_in_schema=False)
def get_overview(request: Request, db: Session = Depends(get_db)):
# tot hier heeft ze geschreven
    lines = db.query(models.Result).all()
    db.close()

    return templates.TemplateResponse(
        "overview.html",
        {
            "request": request,
            "lines": lines,
        },
    )


@app.get("/backup", include_in_schema=False)
def get_backup(request: Request):
    return FileResponse("db/planbord.db", filename="planbord.db")

@app.get("/csv", include_in_schema=False)
def get_csv(request: Request, db: Session = Depends(get_db)):
    csvfilename = "results.csv"
    lines = db.query(models.Result).all()
    db.close()

    with open(csvfilename, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["id", "datum", "symbool", "taak", "makkelijk", "leuk"])
        for line in lines:

            difficultstr = ""
            if line.difficult:
                difficultstr = "moeilijk"
            else:
                difficultstr = "makkelijk"
                
            likestr = ""
            if line.like:
                likestr = "leuk"
            else:
                likestr = "niet leuk"

            csvwriter.writerow(
                [line.id, line.date, line.symbol, line.task, difficultstr, likestr]
            )

    return FileResponse(csvfilename, filename="results.csv")