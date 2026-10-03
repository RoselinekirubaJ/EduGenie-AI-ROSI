from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import (
    QARequest, ExplainRequest, QuizRequest,
    SummaryRequest, LearningPathRequest
)
from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie API",
    description="Google Gemini powered learning assistant",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={"request": request}
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(payload: QARequest):
    return {"result": await answer_question(payload.question)}


@app.post("/explain")
async def explain(payload: ExplainRequest):
    return {"result": await explain_concept(payload.topic, payload.level)}


@app.post("/quiz")
async def quiz(payload: QuizRequest):
    return await generate_quiz(payload.text, payload.num_questions)


@app.post("/summarize")
async def summarize(payload: SummaryRequest):
    return {"result": await summarize_text(payload.text)}


@app.post("/learn/recommendations")
async def recommendations(payload: LearningPathRequest):
    return {"result": await get_learning_recommendations(payload.topic, payload.level)}
