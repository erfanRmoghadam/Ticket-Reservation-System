from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.core.permissions import ensure_owner_or_admin
from src.models.event import Event
from src.models.user import User
from src.repository.event_repository import EventRepository
from src.repository.venue_repository import VenueRepository
from src.repository.category_repository import CategoryRepository
from src.schemas.event import EventCreateRequest, EventUpdateRequest


class EventService:
    def __init__(self, db: Session):
        self.repo = EventRepository(db)
        self.venue_repo = VenueRepository(db)
        self.category_repo = CategoryRepository(db)

    def list_all(self, category_id: int | None, city: str | None, search: str | None) -> list[Event]:
        return self.repo.list_all_events(category_id=category_id, city=city, search=search)

    def get_by_id(self, event_id: int) -> Event:
        event = self.repo.get_event_by_id(event_id)
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found.")
        return event

    def create(self, organizer: User, payload: EventCreateRequest) -> Event:
        if not self.venue_repo.get_venue_by_id(payload.venue_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found.")
        if not self.category_repo.get_category_by_id(payload.category_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")

        event = Event(organizer_id=organizer.user_id, **payload.model_dump())
        return self.repo.create(event)

    def update(self, event_id: int, current_user: User, payload: EventUpdateRequest) -> Event:
        event = self.get_by_id(event_id)
        ensure_owner_or_admin(current_user, event.organizer_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(event, key, value)
        return self.repo.update(event)

    def delete(self, event_id: int, current_user: User) -> None:
        event = self.get_by_id(event_id)
        ensure_owner_or_admin(current_user, event.organizer_id)
        self.repo.delete(event)
