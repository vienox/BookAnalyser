from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.rekomendacje import RekomendacjeRequest, RekomendacjeResponse
from app.services.rekomendacje import przygotuj_rekomendacje

router = APIRouter(prefix="/rekomendacje", tags=["rekomendacje"])


@router.post("", response_model=RekomendacjeResponse)
async def rekomenduj_ksiazki(
    data: RekomendacjeRequest,
    db: AsyncSession = Depends(get_db),
) -> RekomendacjeResponse:
    return await przygotuj_rekomendacje(data, db)
