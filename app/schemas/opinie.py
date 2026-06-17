from pydantic import BaseModel


class OpiniaCreate(BaseModel):
    tresc: str
    autor_typ: str | None = None


class OpiniaRead(BaseModel):
    id: int
    ksiazka_id: int
    tresc: str
    autor_typ: str | None = None

    model_config = {"from_attributes": True}
