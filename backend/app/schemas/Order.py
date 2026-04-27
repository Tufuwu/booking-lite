from pydantic import BaseModel, Field, model_validator
from typing import Annotated

class OrderBase(BaseModel):
    name: Annotated[str, Field(strip_whitespace=True)]
    phone_number: Annotated[str, Field(strip_whitespace=True)]
    room_number: Annotated[str | None, Field(strip_whitespace=True)] = None
    room_id: int | None = None
    stay_length: int = Field(gt=0)

    @model_validator(mode="after")
    def validate_room_reference(self):
        if self.room_number is None and self.room_id is None:
            raise ValueError("room_number or room_id is required")
        return self


class OrderCreate(OrderBase):
    pass


class OrderExtend(BaseModel):
    extra_days: int = Field(gt=0)
