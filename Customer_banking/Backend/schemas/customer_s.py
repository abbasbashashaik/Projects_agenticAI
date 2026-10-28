
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    address: str | None = None


class CustomerCreate(CustomerBase):
    user_id: int


class CustomerUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: date | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    address: str | None = None


class CustomerResponse(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int
    user_id: int
    kyc_status: str
    created_at: datetime
