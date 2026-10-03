import json
import re
from gemini_client import generate_text

def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()

async def generate_quiz(text: str, num_questions: int = 3):
    prompt = f"""
Create exactly {num_questions} multiple-choice questions from the educational text below.
Return ONLY valid JSON, with this shape:
{{
  "questions": [
    {{
      "question": "string",
      "options": ["option A", "option B", "option C", "option D"],
      "answer": "exactly one option string",
      "explanation": "short explanation"
    }}
  ]
}}
Every question must have exactly four options and one correct answer.

Educational text:
{text}
"""
    raw = await generate_text(prompt, temperature=0.2, max_output_tokens=1800)
    try:
        data = json.loads(clean_json_block(raw))
        questions = data.get("questions")
        if not isinstance(questions, list) or len(questions) != num_questions:
            raise ValueError("Unexpected question count.")
        for item in questions:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("options"), list)
                or len(item["options"]) != 4
                or item.get("answer") not in item["options"]
            ):
                raise ValueError("Invalid quiz item structure.")
        return {"questions": questions}
    except Exception as exc:
        return {
            "error": "Quiz generation returned invalid JSON.",
            "details": f"{type(exc).__name__}: {exc}",
            "raw_response": raw,
        }
