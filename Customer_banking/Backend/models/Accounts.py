
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    ForeignKey, String, Numeric, DateTime, func
)
from sqlalchemy.orm import Mapped, mapped_column

from db.connection import Base


class Account(Base):
    __tablename__ = "accounts"

    account_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.customer_id"), nullable=False
    )
    account_number: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False
    )
    account_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="ACTIVE"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False,
        server_default=func.current_timestamp()
    )
