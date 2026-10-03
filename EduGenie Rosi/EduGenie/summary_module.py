from gemini_client import generate_text

async def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational passage for quick revision.
Keep the central facts and ideas, remove repetition, and use clear bullet points
followed by a short overall summary.

Passage:
{text}
"""
    return await generate_text(prompt, temperature=0.2, max_output_tokens=1000)
