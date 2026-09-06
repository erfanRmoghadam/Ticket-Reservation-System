from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class SessionCreateRequest(BaseModel):
    start_time: datetime
    end_time: datetime
    default_price: Decimal #default price applied to every seat of the venue when the session is created


class SessionUpdateRequest(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: str | None = None


class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_id: int
    event_id: int
    start_time: datetime
    end_time: datetime
    status: str


class SessionSeatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_seat_id: int
    seat_id: int
    row_label: str
    seat_number: int
    seat_type: str
    price: Decimal
    status: str
