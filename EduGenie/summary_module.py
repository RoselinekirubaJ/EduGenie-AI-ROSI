from fastapi import HTTPException

from gemini_client import generate_text


async def summarize_text(text: str, max_words: int = 120):
    prompt = f"""
Summarize the following educational passage in no more than {max_words} words.

Preserve:
- the main idea;
- important facts;
- important relationships or steps.

Remove repetition and minor details. Use simple language.

Passage:
{text}
"""

    try:
        summary = generate_text(
            prompt,
            system_instruction=(
                "You are an educational summarization assistant. "
                "Do not introduce information that is absent from the passage."
            ),
            temperature=0.2,
            max_output_tokens=max_words * 2,
        )
        return {"summary": summary}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Summarization failed: {exc}") from exc
