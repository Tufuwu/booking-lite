from pydantic import BaseModel, Field
from typing import Optional, Annotated
from app.db.enums import PaymentStatus

class OrderBase(BaseModel):
    user_id: Annotated[int, Field(gt=0)]
    room_id: Annotated[int, Field(gt=0)]
    check_in_date: Optional[str] = None
    stay_nights: Optional[int] = None

class OrderCreate(OrderBase):
    pass


class OrderOut(OrderBase):
    id: Annotated[int, Field(gt=0)]
    expense: Annotated[float, Field(ge=0.0)]
    payment_status: PaymentStatus
    class Config:
        from_attributes = True