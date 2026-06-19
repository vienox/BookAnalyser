from pydantic import BaseModel


class RaportRead(BaseModel):
    ksiazka_id: int
    raport: str
