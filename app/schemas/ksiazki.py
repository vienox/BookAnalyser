from pydantic import BaseModel, ConfigDict


class KsiazkaCreate(BaseModel):
    tytul: str
    wydawnictwo: str
    przedmiot: str | None = None


class KsiazkaRead(BaseModel):
    id: int
    tytul: str
    wydawnictwo: str
    przedmiot: str | None = None

    model_config = ConfigDict(from_attributes=True)
