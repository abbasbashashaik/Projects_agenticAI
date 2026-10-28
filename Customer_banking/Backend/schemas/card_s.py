
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class CardCreate(BaseModel):
    account_id: int
    card_type: str


class CardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    card_id: int
    account_id: int
    card_number: str
    card_type: str
    expiry_date: date | None = None
    status: str
    created_at: datetime
