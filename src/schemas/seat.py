from pydantic import BaseModel, ConfigDict


class SeatCreateRequest(BaseModel):
    row_label: str
    seat_number: int
    seat_type: str = "normal"


class BulkSeatCreateRequest(BaseModel):
    seats: list[SeatCreateRequest]


class SeatUpdateRequest(BaseModel):
    row_label: str | None = None
    seat_number: int | None = None
    seat_type: str | None = None


class SeatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    seat_id: int
    venue_id: int
    row_label: str
    seat_number: int
    seat_type: str
