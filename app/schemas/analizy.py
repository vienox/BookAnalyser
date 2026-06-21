from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


Sentyment = Literal["Pozytywny", "Negatywny", "Neutralny", "Mieszany"]


class AnalizaAIResult(BaseModel):
    temat: str = Field(min_length=1)
    sentyment: Sentyment
    plus: str = Field(min_length=1)
    minus: str = Field(min_length=1)

    @field_validator("sentyment", mode="before")
    @classmethod
    def normalize_sentyment(cls, value: object) -> object:
        if not isinstance(value, str):
            return value

        normalized = value.strip().lower()
        mapping = {
            "pozytywny": "Pozytywny",
            "pozytywna": "Pozytywny",
            "negatywny": "Negatywny",
            "negatywna": "Negatywny",
            "neutralny": "Neutralny",
            "neutralna": "Neutralny",
            "mieszany": "Mieszany",
            "mieszana": "Mieszany",
        }
        return mapping.get(normalized, value)


class AnalizaRead(BaseModel):
    id: int
    opinia_id: int
    temat: str | None = None
    sentyment: str | None = None
    plus: str | None = None
    minus: str | None = None

    model_config = ConfigDict(from_attributes=True)
