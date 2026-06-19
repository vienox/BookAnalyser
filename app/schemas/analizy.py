from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Sentyment = Literal["Pozytywny", "Negatywny", "Neutralny", "Mieszany"]


class AnalizaAIResult(BaseModel):
    temat: str = Field(min_length=1)
    sentyment: Sentyment
    plus: str = Field(min_length=1)
    minus: str = Field(min_length=1)


class AnalizaRead(BaseModel):
    id: int
    opinia_id: int
    temat: str | None = None
    sentyment: str | None = None
    plus: str | None = None
    minus: str | None = None

    model_config = ConfigDict(from_attributes=True)
