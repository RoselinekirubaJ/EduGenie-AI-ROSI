# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project documentation.

## Features

- Q&A: `/qa`
- Concept explanation: `/explain`
- Three-question MCQ quiz generation: `/quiz`
- Passage summarization: `/summarize`
- Beginner-to-advanced learning recommendations: `/learn/recommendations`
- Browser frontend served by FastAPI
- Gemini integration through the current `google-genai` Python SDK
- Optional local LaMini-Flan-T5 explanation engine

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── schemas.py
├── gemini_client.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── requirements-local-ai.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    ├── conftest.py
    └── test_api.py
```

## 1. Create the environment

Python 3.10+ is recommended.

### Windows

```powershell
py -3.10 -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure Gemini

Copy `.env.example` to `.env` and set:

```env
GEMINI_API_KEY=your_real_key
```

Create the key in Google AI Studio. Never commit `.env`.

## 4. Run

```bash
uvicorn main:app --reload
```

Open:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

## 5. Test

```bash
pytest -q
```

The tests verify routing, validation, frontend delivery, and module integration without making live Gemini requests.

## Optional: local LaMini explanation

The supplied documentation describes LaMini-Flan-T5 as the local explanation model. To enable it:

```bash
pip install -r requirements-local-ai.txt
```

Then set:

```env
USE_LOCAL_EXPLAINER=true
```

The first explanation request downloads the model from Hugging Face and can require substantial disk space and RAM. If the local model is not installed, set `USE_LOCAL_EXPLAINER=false` to use Gemini instead.

## API examples

### Q&A

```bash
curl -X POST http://127.0.0.1:8000/qa ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"What is photosynthesis?\"}"
```

### Explain

```bash
curl -X POST http://127.0.0.1:8000/explain ^
  -H "Content-Type: application/json" ^
  -d "{\"topic\":\"Pythagoras theorem\",\"level\":\"beginner\"}"
```

### Quiz

```bash
curl -X POST http://127.0.0.1:8000/quiz ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"Water freezes at 0 degrees Celsius and boils at 100 degrees Celsius at standard atmospheric pressure.\"}"
```

### Summarize

```bash
curl -X POST http://127.0.0.1:8000/summarize ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"Paste a long educational passage here.\"}"
```

### Learning path

```bash
curl -X POST http://127.0.0.1:8000/learn/recommendations ^
  -H "Content-Type: application/json" ^
  -d "{\"topic\":\"SQL\",\"level\":\"beginner\",\"goal\":\"become job-ready\"}"
```

## Architecture

```text
Browser
  │
  ▼
FastAPI / main.py
  ├── /qa ───────────────► qna.py ───────────────► Gemini
  ├── /explain ──────────► explanation_module.py ─► Gemini or LaMini
  ├── /quiz ─────────────► quiz_module.py ───────► Gemini JSON
  ├── /summarize ────────► summary_module.py ────► Gemini
  └── /learn/recommendations ► learning_path.py ─► Gemini JSON
```

## Notes

The original documentation names Gemini 1.5 Pro. Model availability changes over time, so this implementation makes the Gemini model configurable with `GEMINI_MODEL` instead of hard-coding a retired model name.

The quiz and learning-path modules use structured JSON output and Pydantic validation so malformed model responses fail cleanly rather than breaking the frontend.

For production deployment, add authentication, rate limiting, logging/monitoring, secret management, persistent user progress, and stricter content/safety controls.
