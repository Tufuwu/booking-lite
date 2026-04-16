from typing import Optional, Annotated

from pydantic import BaseModel, Field
from app.utils.regex import IDENTITY_NUMBER_REGEX
from app.db.enums import RoleEnum

class UserBase(BaseModel):
    name: Annotated[str, Field(strip_whitespace=True)]
    phone_number: Annotated[str, Field(strip_whitespace=True)]
    identity_number: Annotated[str, Field(strip_whitespace=True, pattern=IDENTITY_NUMBER_REGEX)]
    role: Annotated[RoleEnum, Field(strip_whitespace=True)]


class UserCreate(UserBase):

    password: Annotated[str, Field(strip_whitespace=True)]


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[Annotated[str, Field(strip_whitespace=True)]] = None
    password: Optional[Annotated[str, Field(strip_whitespace=True)]] = None

class UserDelete(BaseModel):
    password: Annotated[str, Field(strip_whitespace=True)]