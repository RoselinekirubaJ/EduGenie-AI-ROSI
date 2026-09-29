from typing import Optional

from pydantic import BaseModel, Field, field_validator

from config import get_settings


def _clean_text(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("Input cannot be empty.")
    if len(value) > get_settings().MAX_INPUT_CHARS:
        raise ValueError(
            f"Input is too long. Maximum allowed length is "
            f"{get_settings().MAX_INPUT_CHARS} characters."
        )
    return value


class QARequest(BaseModel):
    question: str = Field(..., min_length=1)
    context: Optional[str] = None

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        return _clean_text(value)

    @field_validator("context")
    @classmethod
    def validate_context(cls, value: Optional[str]) -> Optional[str]:
        return _clean_text(value) if value else None


class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    level: str = "beginner"

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: str) -> str:
        return _clean_text(value)


class QuizRequest(BaseModel):
    text: str = Field(..., min_length=1)
    topic: Optional[str] = None

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return _clean_text(value)


class SummaryRequest(BaseModel):
    text: str = Field(..., min_length=1)
    max_words: int = Field(default=120, ge=30, le=500)

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return _clean_text(value)


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    level: str = "beginner"
    goal: Optional[str] = None

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: str) -> str:
        return _clean_text(value)

    @field_validator("goal")
    @classmethod
    def validate_goal(cls, value: Optional[str]) -> Optional[str]:
        return _clean_text(value) if value else None


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion]
