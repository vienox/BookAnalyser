import json

from openai import AsyncOpenAI
from pydantic import ValidationError

from app.schemas.analizy import AnalizaAIResult
from app.settings import settings


class OpenAIConfigError(RuntimeError):
    pass


class OpenAIResponseValidationError(RuntimeError):
    pass


def _get_client() -> AsyncOpenAI:
    if not settings.openai_api_key:
        raise OpenAIConfigError("Brak OPENAI_API_KEY.")

    return AsyncOpenAI(api_key=settings.openai_api_key)


async def analizuj_opinie(tresc: str) -> AnalizaAIResult:
    client = _get_client()
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
    if not content:
        raise OpenAIResponseValidationError("OpenAI zwróciło pustą odpowiedź.")

    try:
        raw_result = json.loads(content)
    except json.JSONDecodeError as exc:
        raise OpenAIResponseValidationError(
            "OpenAI nie zwróciło poprawnego JSON-a."
        ) from exc

    try:
        return AnalizaAIResult.model_validate(raw_result)
    except ValidationError as exc:
        raise OpenAIResponseValidationError(
            "JSON z OpenAI nie pasuje do oczekiwanego formatu."
        ) from exc
