import os
import json
from openai import AsyncOpenAI
from app.core.config import settings

client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL
)

async def analyze_ticket_text(text: str):
    instruction = f"""
    Ти — помічник служби підтримки. Проаналізуй це повідомлення: "{text}"
    Видай відповідь ТІЛЬКИ у форматі JSON з такими полями:
    "category" (bug, question, або feature_request),
    "priority" (low, medium, або high),
    "suggested_response" (коротка ввічлива відповідь клієнту).
    """

    response = await client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[{"role": "user", "content": instruction}],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)