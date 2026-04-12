from pydantic import BaseModel, Field, condecimal
from typing import Optional, Annotated
from decimal import Decimal
from app.db.enums import RoomType
from app.utils import ROOM_NUMBER_REGEX


class RoomBase(BaseModel):
    room_number: Annotated[str, Field(pattern=ROOM_NUMBER_REGEX, strip_whitespace=True)]
    type_: RoomType
    price: Annotated[
        Decimal,
        Field(ge=Decimal("0.00"), max_digits=10, decimal_places=2)
    ]

class RoomCreate(RoomBase):
    pass