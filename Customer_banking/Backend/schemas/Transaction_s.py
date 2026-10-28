
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class TransactionCreate(BaseModel):
    account_id: int
    amount: Decimal
    transaction_type: str
    description: str | None = None


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    transaction_id: int
    account_id: int
    amount: Decimal
    transaction_type: str
    description: str | None
    transaction_date: datetime
