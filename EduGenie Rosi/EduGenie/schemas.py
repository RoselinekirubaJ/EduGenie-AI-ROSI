from pydantic import BaseModel, Field, field_validator
from config import get_settings


def limit_text(value: str) -> str:
    value = value.strip()
    max_chars = get_settings().MAX_INPUT_CHARS
    if not value:
        raise ValueError("Input cannot be empty.")
    if len(value) > max_chars:
        raise ValueError(f"Input is too long. Maximum is {max_chars} characters.")
    return value


class QARequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=20000)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value):
        return limit_text(value)


class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=20000)
    level: str = Field(default="beginner", max_length=50)

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value):
        return limit_text(value)


class QuizRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)
    num_questions: int = Field(default=3, ge=1, le=10)

    @field_validator("text")
    @classmethod
    def validate_text(cls, value):
        return limit_text(value)


class SummaryRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)

    @field_validator("text")
    @classmethod
    def validate_text(cls, value):
        return limit_text(value)


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=20000)
    level: str = Field(default="beginner", max_length=50)

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value):
        return limit_text(value)
