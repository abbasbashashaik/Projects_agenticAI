
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class AccountCreate(BaseModel):
    account_type: str


class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    account_id: int
    customer_id: int
    account_number: str
    account_type: str
    balance: Decimal
    status: str
    created_at: datetime
