# Documentation-to-Code Mapping

The supplied project documentation describes:

- `main.py` — FastAPI application
- `explanation_module.py` — concept explanation
- `qna.py` — question answering
- `quiz_module.py` — quiz generation
- `summary_module.py` — summarization
- `learning_path.py` — recommendations
- `templates/index.html` — frontend
- `static/style.css` — styling
- `requirements.txt` — dependencies

This implementation keeps those modules and adds:

- `config.py` — environment configuration
- `schemas.py` — request/response validation
- `gemini_client.py` — centralized Gemini SDK client
- `static/app.js` — frontend API integration
- `tests/` — automated tests
- `docs/` — API and implementation notes

The documentation says Gemini 1.5 Pro is used for Q&A, summarization, quiz generation, and learning paths, while LaMini-Flan-T5-783M is used for explanation. The implementation preserves that functional split but makes the Gemini model configurable because model names and availability can change.

The documentation also says the quiz should return three MCQs with four options each and JSON output. The implementation enforces those constraints with structured generation and Pydantic validation.
