from fastapi import FastAPI

from app.api.ksiazkiapi import router as ksiazki_router
from app.api.opinieapi import router as opinie_router

app = FastAPI(
    title="Analizator Opinii o Podrecznikach",
    version="0.1.0",
)

app.include_router(ksiazki_router)
app.include_router(opinie_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
