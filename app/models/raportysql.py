from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class AnalizaOpinii(Base):
    __tablename__ = "analizy_opinii"

    id: Mapped[int] = mapped_column(primary_key=True)
    opinia_id: Mapped[int] = mapped_column(
        ForeignKey("opinie.id", ondelete="CASCADE"),
        nullable=False,
    )
    temat: Mapped[str | None] = mapped_column(Text, nullable=True)
    sentyment: Mapped[str | None] = mapped_column(Text, nullable=True)
    plus: Mapped[str | None] = mapped_column(Text, nullable=True)
    minus: Mapped[str | None] = mapped_column(Text, nullable=True)

    opinia: Mapped["Opinia"] = relationship(back_populates="analiza")
