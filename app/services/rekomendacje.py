from collections import defaultdict

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.opinieai import OpenAIConfigError, OpenAIResponseValidationError
from app.ai.rekomendacjeai import dopasuj_rekomendacje_ai
from app.models.ksiazkisql import Ksiazka
from app.models.opiniesql import Opinia
from app.models.raportysql import AnalizaOpinii
from app.schemas.rekomendacje import (
    RekomendacjeRequest,
    RekomendacjeResponse,
    RekomendowanaKsiazka,
)


def _contains_preference(text: str | None, preferences: list[str]) -> bool:
    if not text:
        return False

    normalized_text = text.lower()
    return any(preference.lower() in normalized_text for preference in preferences)


def _unique(values: list[str | None]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []

    for value in values:
        if not value:
            continue

        normalized = value.strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)

    return result


async def przygotuj_rekomendacje(
    data: RekomendacjeRequest,
    db: AsyncSession,
) -> RekomendacjeResponse:
    query = (
        select(Ksiazka, AnalizaOpinii)
        .join(Opinia, Opinia.ksiazka_id == Ksiazka.id)
        .join(AnalizaOpinii, AnalizaOpinii.opinia_id == Opinia.id)
    )

    if data.przedmiot:
        query = query.where(func.lower(Ksiazka.przedmiot) == data.przedmiot.lower())

    result = await db.execute(query)
    rows = result.all()

    grouped: dict[int, dict[str, object]] = defaultdict(
        lambda: {
            "ksiazka": None,
            "analizy": [],
        }
    )

    for ksiazka, analiza in rows:
        grouped[ksiazka.id]["ksiazka"] = ksiazka
        grouped[ksiazka.id]["analizy"].append(analiza)

    rekomendacje: list[RekomendowanaKsiazka] = []

    for item in grouped.values():
        ksiazka = item["ksiazka"]
        analizy = item["analizy"]
        if not isinstance(ksiazka, Ksiazka):
            continue

        plusy = _unique([analiza.plus for analiza in analizy])
        minusy = _unique([analiza.minus for analiza in analizy])

        wynik = 0
        for analiza in analizy:
            if analiza.sentyment == "Pozytywny":
                wynik += 2
            elif analiza.sentyment == "Mieszany":
                wynik += 1
            elif analiza.sentyment == "Negatywny":
                wynik -= 1

            if _contains_preference(analiza.plus, data.preferencje):
                wynik += 3
            if _contains_preference(analiza.temat, data.preferencje):
                wynik += 1
            if _contains_preference(analiza.minus, data.preferencje):
                wynik -= 2

        uzasadnienie = (
            "Dopasowanie policzone na podstawie sentymentu oraz zgodności "
            "plusów i tematów analiz z preferencjami nauczyciela."
        )

        rekomendacje.append(
            RekomendowanaKsiazka(
                ksiazka_id=ksiazka.id,
                tytul=ksiazka.tytul,
                wydawnictwo=ksiazka.wydawnictwo,
                przedmiot=ksiazka.przedmiot,
                wynik=wynik,
                uzasadnienie=uzasadnienie,
                plusy=plusy,
                minusy=minusy,
            )
        )

    rekomendacje.sort(key=lambda item: item.wynik, reverse=True)
    rekomendacje = rekomendacje[: data.limit]

    try:
        ai_rekomendacje = await dopasuj_rekomendacje_ai(data, rekomendacje)
    except (OpenAIConfigError, OpenAIResponseValidationError):
        return RekomendacjeResponse(rekomendacje=rekomendacje, tryb="regulowy")

    return RekomendacjeResponse(rekomendacje=ai_rekomendacje, tryb="ai")
