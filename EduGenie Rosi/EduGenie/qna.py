from gemini_client import generate_text

async def answer_question(question: str) -> str:
    prompt = f"""
You are EduGenie, a helpful educational assistant.
Answer the student's question accurately and concisely.
Use simple language, define important terms, and use a short example when useful.
Do not invent citations or claim certainty when the answer is uncertain.

Student question:
{question}
"""
    return await generate_text(prompt, temperature=0.2, max_output_tokens=900)
