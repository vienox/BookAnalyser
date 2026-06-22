import json

from openai import AsyncOpenAI

from app.ai.opinieai import OpenAIConfigError, OpenAIResponseValidationError
from app.schemas.rekomendacje import RekomendacjeRequest, RekomendowanaKsiazka
from app.settings import settings


def _get_client() -> AsyncOpenAI:
    if not settings.openai_api_key:
        raise OpenAIConfigError("Brak OPENAI_API_KEY.")

    return AsyncOpenAI(api_key=settings.openai_api_key)


async def dopasuj_rekomendacje_ai(
    data: RekomendacjeRequest,
    kandydaci: list[RekomendowanaKsiazka],
) -> list[RekomendowanaKsiazka]:
    client = _get_client()
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": (
                    "Jesteś doradcą metodycznym pomagającym nauczycielowi "
                    "wybrać podręcznik. Dostaniesz profil nauczyciela, "
                    "preferencje i kandydatów z punktacją regułową. "
                    "Zwróć wyłącznie JSON z polem rekomendacje. "
                    "Każda rekomendacja musi mieć pola: ksiazka_id, "
                    "uzasadnienie."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "profil_nauczyciela": data.profil_nauczyciela,
                        "przedmiot": data.przedmiot,
                        "preferencje": data.preferencje,
                        "kandydaci": [
                            kandydat.model_dump() for kandydat in kandydaci
                        ],
                    },
                    ensure_ascii=False,
                ),
            },
        ],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    if not content:
        raise OpenAIResponseValidationError("OpenAI zwróciło pustą odpowiedź.")

    try:
        raw_result = json.loads(content)
    except json.JSONDecodeError as exc:
        raise OpenAIResponseValidationError(
            "OpenAI nie zwróciło poprawnego JSON-a."
        ) from exc

    ai_rekomendacje = raw_result.get("rekomendacje")
    if not isinstance(ai_rekomendacje, list):
        raise OpenAIResponseValidationError(
            "JSON z OpenAI nie zawiera listy rekomendacje."
        )

    by_id = {kandydat.ksiazka_id: kandydat for kandydat in kandydaci}
    result: list[RekomendowanaKsiazka] = []

    for item in ai_rekomendacje:
        if not isinstance(item, dict):
            continue

        ksiazka_id = item.get("ksiazka_id")
        uzasadnienie = item.get("uzasadnienie")
        if not isinstance(ksiazka_id, int) or not isinstance(uzasadnienie, str):
            continue

        kandydat = by_id.get(ksiazka_id)
        if kandydat is None:
            continue

        result.append(kandydat.model_copy(update={"uzasadnienie": uzasadnienie}))

    if not result:
        raise OpenAIResponseValidationError(
            "OpenAI nie zwróciło żadnej poprawnej rekomendacji."
        )

    return result
