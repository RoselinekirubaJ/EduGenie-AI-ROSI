from gemini_client import generate_text

async def get_learning_recommendations(topic: str, level: str = "beginner") -> str:
    prompt = f"""
Create a personalized learning path for the topic below for a {level} learner.
Organize it from beginner to advanced.
For each stage include:
1. Topics to learn
2. Suggested practice
3. A realistic timeline
4. Useful resource types (videos, articles, books, documentation)
5. A simple milestone to check progress

Topic: {topic}

Be practical and avoid inventing specific URLs.
"""
    return await generate_text(prompt, temperature=0.35, max_output_tokens=1600)
