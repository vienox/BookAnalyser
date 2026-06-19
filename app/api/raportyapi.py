from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.opinieai import OpenAIConfigError
from app.ai.raportyai import generuj_raport
from app.database.session import get_db
from app.models.ksiazkisql import Ksiazka
from app.models.opiniesql import Opinia
from app.models.raportysql import AnalizaOpinii
from app.schemas.raporty import RaportRead

router = APIRouter(prefix="/ksiazki", tags=["raporty"])


@router.get("/{ksiazka_id}/raport", response_model=RaportRead)
async def get_raport(
    ksiazka_id: int,
    db: AsyncSession = Depends(get_db),
) -> RaportRead:
    ksiazka = await db.get(Ksiazka, ksiazka_id)
    if ksiazka is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ksiazka nie istnieje.",
        )

    result = await db.execute(
        select(AnalizaOpinii)
        .join(Opinia, AnalizaOpinii.opinia_id == Opinia.id)
        .where(Opinia.ksiazka_id == ksiazka_id)
        .order_by(AnalizaOpinii.id)
    )
    analizy = list(result.scalars().all())

    if not analizy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brak analiz opinii dla tej ksiazki.",
        )

    dane_analiz = [
        {
            "temat": analiza.temat,
            "sentyment": analiza.sentyment,
            "plus": analiza.plus,
            "minus": analiza.minus,
        }
        for analiza in analizy
    ]

    try:
        raport = await generuj_raport(dane_analiz)
    except OpenAIConfigError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    return RaportRead(ksiazka_id=ksiazka_id, raport=raport)
