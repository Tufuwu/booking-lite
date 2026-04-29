from datetime import date, timedelta
from typing import Annotated

from pydantic import BaseModel, Field, model_validator


class OrderBase(BaseModel):
    name: Annotated[str, Field(strip_whitespace=True)]
    phone_number: Annotated[str, Field(strip_whitespace=True)]
    room_number: Annotated[str | None, Field(strip_whitespace=True)] = None
    room_id: int | None = None
    check_in_date: date = Field(default_factory=date.today)
    check_out_date: date | None = None
    stay_length: int | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def validate_order_dates(self):
        if self.room_number is None and self.room_id is None:
            raise ValueError("room_number or room_id is required")

        if self.check_out_date is None and self.stay_length is None:
            raise ValueError("check_out_date or stay_length is required")

        if self.check_out_date is None:
            self.check_out_date = self.check_in_date + timedelta(days=self.stay_length)

        if self.check_out_date <= self.check_in_date:
            raise ValueError("check_out_date must be after check_in_date")

        if self.stay_length is None:
            self.stay_length = (self.check_out_date - self.check_in_date).days

        return self


class OrderCreate(OrderBase):
    pass


class OrderExtend(BaseModel):
    extra_days: int = Field(gt=0)
