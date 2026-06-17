from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Ksiazka(Base):
    __tablename__ = "ksiazki"

    id: Mapped[int] = mapped_column(primary_key=True)
    tytul: Mapped[str] = mapped_column(Text, nullable=False)
    wydawnictwo: Mapped[str] = mapped_column(Text, nullable=False)
    przedmiot: Mapped[str | None] = mapped_column(Text, nullable=True)

    opinie: Mapped[list["Opinia"]] = relationship(
        back_populates="ksiazka",
        cascade="all, delete-orphan",
    )
