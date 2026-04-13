from pydantic import BaseModel, Field
from typing import Annotated, Optional
from app.utils.regex import IDENTITY_NUMBER_REGEX

class UserBase(BaseModel):
    name: Annotated[str, Field(strip_whitespace=True)]
    phone_number: Annotated[str, Field(strip_whitespace=True)]
    identity_number: Annotated[str, Field(strip_whitespace=True, pattern=IDENTITY_NUMBER_REGEX)]


class UserCreate(UserBase):
    password: Annotated[str, Field(strip_whitespace=True)]

class UserOut(UserBase):
    id: int
    orders: list = []
    class Config:
        from_attributes = True