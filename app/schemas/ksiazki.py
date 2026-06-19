from pydantic import BaseModel


class KsiazkaCreate(BaseModel):
    tytul: str
    wydawnictwo: str
    przedmiot: str | None = None


class KsiazkaRead(BaseModel):
    id: int
    tytul: str
    wydawnictwo: str
    przedmiot: str | None = None