"""OpenAI client utilities for generating AI responses."""

from groq import Groq
from django.conf import settings

# Initialize Groq client
client = Groq(api_key=settings.GROQ_API_KEY)

# Model you selected
MODEL_NAME = "openai/gpt-oss-120b"


def get_ai_reply(prompt: str) -> str:
    """Generate an AI response for the given prompt.
    Args:
        prompt (str): User input or constructed prompt.

    Returns:
        str: AI-generated response or error message.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=512,
        )

        return response.choices[0].message.content.strip()

    except Exception as e: # pylint: disable=broad-exception-caught
        return f"⚠️ Groq Error: {str(e)}"
