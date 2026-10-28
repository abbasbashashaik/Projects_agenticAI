
from datetime import date, datetime

from sqlalchemy import (
    ForeignKey, String, Date, DateTime, func
)
from sqlalchemy.orm import Mapped, mapped_column

from db.connection import Base


class Card(Base):
    __tablename__ = "cards"

    card_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.account_id"), nullable=False
    )
    card_number: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False
    )
    card_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )
    expiry_date: Mapped[date | None] = mapped_column(
        Date, nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="ACTIVE"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False,
        server_default=func.current_timestamp()
    )
