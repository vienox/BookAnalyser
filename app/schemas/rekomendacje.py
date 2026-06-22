from pydantic import BaseModel, Field


class RekomendacjeRequest(BaseModel):
    przedmiot: str | None = None
    profil_nauczyciela: str | None = None
    preferencje: list[str] = Field(default_factory=list)
    limit: int = Field(default=3, ge=1, le=10)


class RekomendowanaKsiazka(BaseModel):
    ksiazka_id: int
    tytul: str
    wydawnictwo: str
    przedmiot: str | None = None
    wynik: int
    uzasadnienie: str
    plusy: list[str]
    minusy: list[str]


class RekomendacjeResponse(BaseModel):
    rekomendacje: list[RekomendowanaKsiazka]
    tryb: str = "regulowy"
