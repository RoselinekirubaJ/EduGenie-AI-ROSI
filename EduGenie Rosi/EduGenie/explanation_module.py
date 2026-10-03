from gemini_client import generate_text
from config import get_settings

async def _gemini_explanation(topic: str, level: str) -> str:
    prompt = f"""
Explain the following concept for a {level} learner.
Start with a one-sentence definition, then explain it in small steps.
Use an everyday analogy or simple example when helpful.
Avoid unnecessary jargon.

Concept: {topic}
"""
    return await generate_text(prompt, temperature=0.25, max_output_tokens=900)


async def explain_concept(topic: str, level: str = "beginner") -> str:
    # The project documentation specifies LaMini-Flan-T5 for explanation.
    # It is optional because loading a local Transformer model requires a
    # large first-time download. Gemini remains the reliable default.
    settings = get_settings()
    if settings.USE_LOCAL_EXPLAINER:
        try:
            from transformers import pipeline
            generator = pipeline(
                "text2text-generation",
                model=settings.LOCAL_EXPLAINER_MODEL,
                device=-1,
            )
            prompt = (
                f"Explain {topic} to a {level} learner simply, "
                "with a definition, steps, and a short example."
            )
            result = generator(prompt, max_new_tokens=300)
            return result[0]["generated_text"].strip()
        except Exception as exc:
            return (
                "The optional local LaMini explainer could not be loaded. "
                f"Falling back to Gemini. Reason: {type(exc).__name__}: {exc}\n\n"
                + await _gemini_explanation(topic, level)
            )
    return await _gemini_explanation(topic, level)
