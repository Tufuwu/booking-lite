from typing import Optional, Annotated

from pydantic import BaseModel, Field



class AdminBase(BaseModel):
    job_number: Annotated[str, Field(strip_whitespace=True)]
    name: Annotated[str, Field(strip_whitespace=True)]



class AdminCreate(AdminBase):
    password: Annotated[str, Field(strip_whitespace=True)]


class AdminOut(AdminBase):
    id: int

    class Config:
        from_attributes = True

class AdminDelete(BaseModel):
    password: Annotated[str, Field(strip_whitespace=True)]