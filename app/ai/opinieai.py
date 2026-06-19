import json

from openai import AsyncOpenAI

from app.settings import settings

client = AsyncOpenAI(api_key=settings.openai_api_key)


async def analizuj_opinie(tresc: str) -> dict:
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "Przeanalizuj opinię użytkownika. "
                    "Zwróć wyłącznie poprawny JSON z polami: "
                    "temat, sentyment, plus, minus."
                ),
            },
            {
                "role": "user",
                "content": tresc,
            },
        ],
    )

    content = response.choices[0].message.content
    return json.loads(content)