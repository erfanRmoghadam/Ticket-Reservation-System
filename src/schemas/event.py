from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventCreateRequest(BaseModel):
    category_id: int
    venue_id: int
    title: str
    description: str | None = None
    cover_image_url: str | None = None


class EventUpdateRequest(BaseModel):
    category_id: int | None = None
    title: str | None = None
    description: str | None = None
    cover_image_url: str | None = None


class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    event_id: int
    organizer_id: int
    category_id: int
    venue_id: int
    title: str
    description: str | None = None
    cover_image_url: str | None = None
    created_at: datetime
