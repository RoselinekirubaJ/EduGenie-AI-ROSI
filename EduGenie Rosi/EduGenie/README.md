# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a FastAPI + HTML/CSS/JavaScript educational assistant based on the supplied project documentation.

## Features

- Question answering (`/qa`)
- Simplified concept explanation (`/explain`)
- Multiple-choice quiz generation (`/quiz`)
- Educational text summarization (`/summarize`)
- Beginner-to-advanced learning paths (`/learn/recommendations`)
- Responsive browser frontend
- Health check endpoint (`/health`)

The documentation specifies Gemini for Q&A, quizzes, summaries and learning paths, and LaMini-Flan-T5-783M for concept explanation. The implementation keeps that design: the local LaMini model is optional, while Gemini is the default explanation backend so the project can run without downloading a large local model.

## 1. Create the environment

### Windows PowerShell

```powershell
cd F:\EduGenie
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If your project is stored somewhere else, replace `F:\EduGenie` with that folder.

## 2. Configure Gemini

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace:

```text
GEMINI_API_KEY=PASTE_YOUR_GEMINI_API_KEY_HERE
```

with your actual key.

Do not commit `.env` to Git. It is already ignored by `.gitignore`.

## 3. Start the application

Always activate the environment first in a new PowerShell window:

```powershell
cd F:\EduGenie
.\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload
```

Open:

http://127.0.0.1:8000

API documentation is available at:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

## 4. Test

With the server running:

```powershell
pytest -q
```

For a manual browser test:
1. Choose "Ask a Question".
2. Enter: `Which is the largest ocean?`
3. Click "Generate Result".
4. Try each of the other four tasks.

## 5. Optional LaMini local explanation

The project documentation names `MBZUAI/LaMini-Flan-T5-783M` for concept explanation. To use it locally, install the optional dependencies:

```powershell
pip install transformers torch
```

Then change `.env`:

```text
USE_LOCAL_EXPLAINER=true
```

The first local-model use can download model files and may require substantial disk/RAM. If it fails, EduGenie falls back to Gemini.

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── schemas.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    └── test_api.py
```

## Common Windows issue

If `uvicorn` is not recognized, do not use the bare command. Activate `.venv` and run:

```powershell
python -m uvicorn main:app --reload
```

This ensures Uvicorn is taken from the active virtual environment.

## API examples

### Q&A

```json
POST /qa
{
  "question": "What is photosynthesis?"
}
```

### Explain

```json
POST /explain
{
  "topic": "Pythagoras theorem",
  "level": "beginner"
}
```

### Quiz

```json
POST /quiz
{
  "text": "The Earth revolves around the Sun.",
  "num_questions": 3
}
```

### Summary

```json
POST /summarize
{
  "text": "Long educational passage..."
}
```

### Learning path

```json
POST /learn/recommendations
{
  "topic": "SQL",
  "level": "beginner"
}
```
