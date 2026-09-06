from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ReservationCreateRequest(BaseModel):
    session_id: int
    seat_ids: list[int]


class ReservationItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reservation_item_id: int
    session_seat_id: int
    price: Decimal


class ReservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reservation_id: int
    user_id: int
    session_id: int
    status: str
    total_price: Decimal
    expires_at: datetime
    created_at: datetime
    items: list[ReservationItemResponse] = []
