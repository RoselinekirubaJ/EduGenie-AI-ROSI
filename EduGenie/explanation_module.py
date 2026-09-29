from fastapi import HTTPException

from config import get_settings
from gemini_client import generate_text


_local_pipeline = None


def _get_local_pipeline():
    global _local_pipeline
    if _local_pipeline is None:
        try:
            from transformers import pipeline
        except ImportError as exc:
            raise RuntimeError(
                "Local explanation requires transformers. "
                "Install requirements-local-ai.txt or set USE_LOCAL_EXPLAINER=false."
            ) from exc

        _local_pipeline = pipeline(
            "text2text-generation",
            model=get_settings().LOCAL_EXPLAINER_MODEL,
        )
    return _local_pipeline


async def explain_concept(topic: str, level: str = "beginner"):
    settings = get_settings()
    prompt = f"""
Explain the educational topic "{topic}" for a {level} learner.

Structure:
1. Simple definition
2. How it works
3. One intuitive example
4. Three key points to remember

Use clear language and avoid unnecessary jargon.
"""

    try:
        if settings.USE_LOCAL_EXPLAINER:
            generator = _get_local_pipeline()
            result = generator(
                prompt,
                max_new_tokens=350,
                do_sample=False,
            )
            answer = result[0]["generated_text"].strip()
            engine = "LaMini-Flan-T5 (local)"
        else:
            answer = generate_text(
                prompt,
                system_instruction=(
                    "You simplify difficult concepts for students. "
                    "Prefer short paragraphs, examples, and plain language."
                ),
                temperature=0.25,
                max_output_tokens=700,
            )
            engine = f"Gemini ({settings.GEMINI_MODEL})"

        return {"explanation": answer, "engine": engine}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=502, detail=f"Explanation generation failed: {exc}"
        ) from exc
