from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.ksiazkisql import Ksiazka
from app.schemas.ksiazki import KsiazkaCreate, KsiazkaRead

router = APIRouter(prefix="/ksiazki", tags=["ksiazki"])


@router.post("", response_model=KsiazkaRead, status_code=status.HTTP_201_CREATED)
async def create_ksiazka(
    data: KsiazkaCreate,
    db: AsyncSession = Depends(get_db),
) -> Ksiazka:
    ksiazka = Ksiazka(
        tytul=data.tytul,
        wydawnictwo=data.wydawnictwo,
        przedmiot=data.przedmiot,
    )

    db.add(ksiazka)
    await db.commit()
    await db.refresh(ksiazka)

    return ksiazka


@router.get("", response_model=list[KsiazkaRead])
async def list_ksiazki(db: AsyncSession = Depends(get_db)) -> list[Ksiazka]:
    result = await db.execute(select(Ksiazka).order_by(Ksiazka.id))
    return list(result.scalars().all())


@router.get("/{ksiazka_id}", response_model=KsiazkaRead)
async def get_ksiazka(
    ksiazka_id: int,
    db: AsyncSession = Depends(get_db),
) -> Ksiazka:
    ksiazka = await db.get(Ksiazka, ksiazka_id)
    if ksiazka is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ksiazka nie istnieje.",
        )

    return ksiazka
