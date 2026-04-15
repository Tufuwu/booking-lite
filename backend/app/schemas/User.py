from typing import Optional, Annotated

from pydantic import BaseModel, Field
from app.utils.regex import IDENTITY_NUMBER_REGEX


class UserBase(BaseModel):
    job_number: Annotated[str, Field(strip_whitespace=True)]
    name: Annotated[str, Field(strip_whitespace=True)]
    identity_number: Annotated[str, Field(strip_whitespace=True, pattern=IDENTITY_NUMBER_REGEX)]


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