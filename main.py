from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from engine import analyze

BASE_DIR = Path(__file__).parent

app = FastAPI(title="Grammar & Spelling Checker")


class CheckRequest(BaseModel):
    text: str = Field(..., max_length=5000)


@app.post("/api/check")
def check(req: CheckRequest):
    return analyze(req.text)


@app.get("/api/health")
def health():
    return {"status": "ok"}


app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")