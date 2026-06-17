from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Opinia(Base):
    __tablename__ = "opinie"

    id: Mapped[int] = mapped_column(primary_key=True)
    ksiazka_id: Mapped[int] = mapped_column(
        ForeignKey("ksiazki.id", ondelete="CASCADE"),
        nullable=False,
    )
    tresc: Mapped[str] = mapped_column(Text, nullable=False)
    autor_typ: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_dodania: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.current_timestamp(),
        nullable=False,
    )

    ksiazka: Mapped["Ksiazka"] = relationship(back_populates="opinie")
    analiza: Mapped["AnalizaOpinii | None"] = relationship(
        back_populates="opinia",
        cascade="all, delete-orphan",
        uselist=False,
    )
