
from datetime import date, datetime

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from db.connection import Base
from models.user import User

class Customer(Base):
    __tablename__ = "customers"
    
    customer_id: Mapped[str] = mapped_column(
        String(10), primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.id),
        unique=True,
        nullable=False,
    )

    first_name: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    date_of_birth: Mapped[date | None] = mapped_column(
        Date, nullable=True
    )

    email: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )

    phone_number: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )

    address: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )

    kyc_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="PENDING"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )
