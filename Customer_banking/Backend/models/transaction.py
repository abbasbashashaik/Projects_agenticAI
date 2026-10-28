
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    ForeignKey, String, Numeric, DateTime, func
)
from sqlalchemy.orm import Mapped, mapped_column

from db.connection import Base


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[str] = mapped_column(
       String(10),primary_key=True
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.account_id"), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False
    )
    transaction_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    transaction_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False,
        server_default=func.current_timestamp()
    )
