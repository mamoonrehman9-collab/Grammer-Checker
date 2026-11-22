from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from engine import analyze

BASE_DIR = Path(__file__).parent
PUBLIC_DIR = BASE_DIR / "public"

app = FastAPI(title="Grammar & Spelling Checker")


class CheckRequest(BaseModel):
    text: str = Field(..., max_length=5000)


@app.post("/api/check")
def check(req: CheckRequest):
    return analyze(req.text)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/")
def home():
    return FileResponse(PUBLIC_DIR / "index.html")