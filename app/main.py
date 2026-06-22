from fastapi import FastAPI

from app.api.analizyapi import router as analizy_router
from app.api.ksiazkiapi import router as ksiazki_router
from app.api.opinieapi import router as opinie_router
from app.api.raportyapi import router as raporty_router
from app.api.rekomendacjeapi import router as rekomendacje_router


app = FastAPI(
    title="Analizator Opinii o Podrecznikach",
    version="0.1.0",
)

app.include_router(ksiazki_router)
app.include_router(opinie_router)
app.include_router(analizy_router)
app.include_router(raporty_router)
app.include_router(rekomendacje_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
