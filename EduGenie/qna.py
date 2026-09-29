from fastapi import HTTPException

from gemini_client import generate_text


async def answer_question(question: str, context: str | None = None):
    prompt = f"""
Answer the student's question accurately and educationally.

Question:
{question}
"""
    if context:
        prompt += f"""
Use this context when relevant:
{context}
"""

    prompt += """
Requirements:
- Give the direct answer first.
- Explain the reasoning in simple language.
- If the question is ambiguous, state the assumption you made.
- Do not invent sources, citations, or facts.
- Keep the answer concise unless more detail is necessary.
"""

    try:
        answer = generate_text(
            prompt,
            system_instruction=(
                "You are EduGenie, a careful educational assistant. "
                "Teach clearly, avoid unnecessary jargon, and acknowledge uncertainty."
            ),
            temperature=0.2,
            max_output_tokens=800,
        )
        return {"answer": answer}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Q&A generation failed: {exc}") from exc
