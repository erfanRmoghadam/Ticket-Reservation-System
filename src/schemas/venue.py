from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VenueCreateRequest(BaseModel):
    name: str
    address: str
    city: str
    total_capacity: int


class VenueUpdateRequest(BaseModel):
    name: str | None = None
    address: str | None = None
    city: str | None = None
    total_capacity: int | None = None


class VenueResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    venue_id: int
    name: str
    address: str
    city: str
    total_capacity: int
    created_at: datetime
