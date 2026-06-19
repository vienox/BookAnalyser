from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.opinie import analizuj_opinie
from app.database.session import get_db
from app.models.opiniesql import Opinia
from app.models.raportysql import AnalizaOpinii
from app.schemas.analizy import AnalizaRead

router = APIRouter(prefix="/opinie", tags=["analizy"])


@router.post("/{opinia_id}/analizuj", response_model=AnalizaRead)
async def analizuj_opinie_endpoint(
    opinia_id: int,
    db: AsyncSession = Depends(get_db),
) -> AnalizaOpinii:
    opinia = await db.get(Opinia, opinia_id)

    if opinia is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opinia nie istnieje.",
        )

    wynik = await analizuj_opinie(opinia.tresc)

    analiza = AnalizaOpinii(
        opinia_id=opinia.id,
        temat=wynik.get("temat"),
        sentyment=wynik.get("sentyment"),
        plus=wynik.get("plus"),
        minus=wynik.get("minus"),
    )

    db.add(analiza)
    await db.commit()
    await db.refresh(analiza)

    return analiza