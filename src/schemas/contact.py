from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from src.schemas.user import UserResponse


class ContactSchema(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    phone_number: str = Field(default=12)
    born_date: str = Field(min_length=5, max_length=20)
    completed: Optional[bool] = False


class ContactUpdateSchema(ContactSchema):
    completed: bool


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    born_date: str
    completed: bool
    created_at: datetime | None
    updated_at: datetime | None
    user: UserResponse | None

    class Config:
        from_attributes = True
