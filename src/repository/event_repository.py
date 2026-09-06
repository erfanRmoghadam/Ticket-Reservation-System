from sqlalchemy.orm import Session

from src.models.event import Event
from src.models.venue import Venue


class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all_events(
        self,
        category_id: int | None = None,
        city: str | None = None,
        search: str | None = None,
    ) -> list[Event]:
        query = self.db.query(Event)
        if category_id:
            query = query.filter(Event.category_id == category_id)
        if search:
            query = query.filter(Event.title.ilike(f"%{search}%"))
        if city:
            query = query.join(Event.venue).filter(Event.venue.has(Venue.city.ilike(f"%{city}%")))
        return query.order_by(Event.created_at.desc()).all()

    def get_event_by_id(self, event_id: int) -> Event | None:
        return self.db.query(Event).filter(Event.event_id == event_id).first()
    
    def create(self, event: Event) -> Event:
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def update(self, event: Event) -> Event:
        self.db.commit()
        self.db.refresh(event)
        return event

    def delete(self, event: Event) -> None:
        self.db.delete(event)
        self.db.commit()
