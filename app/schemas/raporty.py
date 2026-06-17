from pydantic import BaseModel

class RaportCreate(BaseModel):
    tytul: str
    tresc: str
    ksiazka_id: int

class RaportRead(BaseModel):
    id: int
    tytul: str
    tresc: str

    