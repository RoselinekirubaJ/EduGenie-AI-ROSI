from fastapi import HTTPException
from pydantic import BaseModel, Field

from gemini_client import generate_text


class QuizItem(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class QuizPayload(BaseModel):
    questions: list[QuizItem] = Field(min_length=3, max_length=3)


async def generate_quiz(text: str, topic: str | None = None):
    topic_hint = f" Topic: {topic}." if topic else ""
    prompt = f"""
Create exactly 3 multiple-choice questions from the educational material below.{topic_hint}

Material:
{text}

For every question:
- provide exactly 4 options;
- make exactly one option correct;
- make distractors plausible but clearly wrong;
- provide a short explanation of the correct answer.
"""

    try:
        raw = generate_text(
            prompt,
            system_instruction=(
                "You are a quiz generator. Return only data matching the requested "
                "JSON schema. Never add markdown fences."
            ),
            temperature=0.4,
            max_output_tokens=1200,
            response_schema=QuizPayload,
        )
        payload = QuizPayload.model_validate_json(raw)
        return payload.model_dump()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Quiz generation failed: {exc}") from exc
