from datetime import datetime
from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from db.connection import engine

class Base(DeclarativeBase):
    pass


class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
  username: Mapped[str] = mapped_column(
      String(50), unique=True, index=True, nullable=False
  )
  email: Mapped[str] = mapped_column(
      String(100), unique=True, index=True, nullable=False
  )
  password: Mapped[str] = mapped_column(
      String(100), nullable=False
  )  # Plain text password
  created_at: Mapped[datetime] = mapped_column(
      DateTime(timezone=True), server_default=func.now()
  )
Base.metadata.create_all(bind=engine)