from pydantic import BaseModel

class OpinieCreate(BaseModel):
    tytul: str
    tresc: str
    ocena: int
    ksiazka_id: int

class OpinieRead(BaseModel):
    id: int
    tytul: str
    tresc: str
    ocena: int