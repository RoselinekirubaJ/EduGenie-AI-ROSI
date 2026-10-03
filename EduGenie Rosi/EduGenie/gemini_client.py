from functools import lru_cache
from fastapi import HTTPException
from google import genai

from config import get_settings


@lru_cache
def get_client():
    settings = get_settings()
    if not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail=(
                "GEMINI_API_KEY is not configured. Create a .env file from "
                ".env.example and add your Google Gemini API key."
            ),
        )
    return genai.Client(api_key=settings.GEMINI_API_KEY)


async def generate_text(prompt: str, temperature: float = 0.3, max_output_tokens: int = 1000) -> str:
    settings = get_settings()
    client = get_client()
    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config={
                "temperature": temperature,
                "max_output_tokens": max_output_tokens,
            },
        )
        text = getattr(response, "text", None)
        if not text:
            raise HTTPException(
                status_code=502,
                detail="Gemini returned an empty response."
            )
        return text.strip()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Gemini request failed: {type(exc).__name__}: {exc}"
        ) from exc
