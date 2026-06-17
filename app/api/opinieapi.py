from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.ksiazkisql import Ksiazka
from app.models.opiniesql import Opinia
from app.schemas.opinie import OpiniaCreate, OpiniaRead

router = APIRouter(prefix="/ksiazki/{ksiazka_id}/opinie", tags=["opinie"])


@router.post("", response_model=OpiniaRead, status_code=status.HTTP_201_CREATED)
async def create_opinia(
    ksiazka_id: int,
    data: OpiniaCreate,
    db: AsyncSession = Depends(get_db),
) -> Opinia:
    ksiazka = await db.get(Ksiazka, ksiazka_id)
    if ksiazka is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ksiazka nie istnieje.",
        )

    opinia = Opinia(
        ksiazka_id=ksiazka_id,
        tresc=data.tresc,
        autor_typ=data.autor_typ,
    )

    db.add(opinia)
    await db.commit()
    await db.refresh(opinia)

    return opinia


@router.get("", response_model=list[OpiniaRead])
async def list_opinie(
    ksiazka_id: int,
    db: AsyncSession = Depends(get_db),
) -> list[Opinia]:
    ksiazka = await db.get(Ksiazka, ksiazka_id)
    if ksiazka is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ksiazka nie istnieje.",
        )

    result = await db.execute(
        select(Opinia)
        .where(Opinia.ksiazka_id == ksiazka_id)
        .order_by(Opinia.id)
    )
    return list(result.scalars().all())
