from pydantic import BaseModel, ConfigDict


class AnalizaRead(BaseModel):
    id: int
    opinia_id: int
    temat: str | None = None
    sentyment: str | None = None
    plus: str | None = None
    minus: str | None = None

    model_config = ConfigDict(from_attributes=True)