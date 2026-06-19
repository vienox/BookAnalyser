from openai import AsyncOpenAI

from app.ai.opinieai import OpenAIConfigError
from app.settings import settings


def _get_client() -> AsyncOpenAI:
    if not settings.openai_api_key:
        raise OpenAIConfigError("Brak OPENAI_API_KEY.")

    return AsyncOpenAI(api_key=settings.openai_api_key)


async def generuj_raport(analizy: list[dict[str, str | None]]) -> str:
    client = _get_client()
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": (
                    "Jesteś analitykiem produktu edukacyjnego. "
                    "Na podstawie danych przygotuj raport dla wydawnictwa. "
                    "Uwzględnij najczęściej chwalone elementy, najczęściej "
                    "zgłaszane problemy, rekomendacje zmian i krótkie "
                    "podsumowanie."
                ),
            },
            {
                "role": "user",
                "content": str(analizy),
            },
        ],
    )

    content = response.choices[0].message.content
    if not content:
        return "Nie udało się wygenerować raportu."

    return content
