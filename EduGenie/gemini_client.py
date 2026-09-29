from functools import lru_cache

from fastapi import HTTPException
from google import genai
from google.genai import types

from config import get_settings


@lru_cache
def get_client() -> genai.Client:
    settings = get_settings()
    if not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail=(
                "GEMINI_API_KEY is not configured. Copy .env.example to .env "
                "and add your Google Gemini API key."
            ),
        )
    return genai.Client(api_key=settings.GEMINI_API_KEY)


def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.3,
    max_output_tokens: int = 1000,
    response_schema=None,
) -> str:
    settings = get_settings()
    client = get_client()

    config_kwargs = {
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
    }
    if system_instruction:
        config_kwargs["system_instruction"] = system_instruction
    if response_schema is not None:
        config_kwargs["response_mime_type"] = "application/json"
        config_kwargs["response_schema"] = response_schema

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(**config_kwargs),
    )

    text = response.text
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
