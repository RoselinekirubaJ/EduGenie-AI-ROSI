from fastapi import HTTPException
from pydantic import BaseModel, Field

from gemini_client import generate_text


class LearningStep(BaseModel):
    stage: str
    topics: list[str]
    suggested_duration: str
    activities: list[str]
    resources: list[str]


class LearningPath(BaseModel):
    title: str
    goal: str
    overview: str
    steps: list[LearningStep] = Field(min_length=3)
    study_tips: list[str]


async def get_learning_recommendations(
    topic: str, level: str = "beginner", goal: str | None = None
):
    learner_goal = goal or f"build strong practical knowledge of {topic}"
    prompt = f"""
Create a structured learning path for "{topic}" for a {level} learner.

Learner goal: {learner_goal}

Progress from beginner to advanced. Include:
- ordered stages;
- topics for each stage;
- realistic study duration;
- practical activities;
- resource suggestions (resource names/types, not fabricated URLs);
- concise study tips.

Keep the path achievable and educationally coherent.
"""

    try:
        raw = generate_text(
            prompt,
            system_instruction=(
                "You are an educational curriculum designer. "
                "Return only JSON matching the requested schema. "
                "Never invent specific URLs."
            ),
            temperature=0.35,
            max_output_tokens=1800,
            response_schema=LearningPath,
        )
        path = LearningPath.model_validate_json(raw)
        return path.model_dump()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=502, detail=f"Learning path generation failed: {exc}"
        ) from exc
