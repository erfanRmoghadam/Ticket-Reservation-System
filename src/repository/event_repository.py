from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.models.event import Event
from src.models.venue import Venue


SORTABLE_FIELDS = {"created_at": Event.created_at,"title": Event.title}

class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def search(
    self,
    category_id: int | None = None,
    city: str | None = None,
    search: str | None = None,
    sort_by: str = "created_at",
    order: str = "desc",
    offset: int = 0,
    limit: int = 20,
) -> tuple[list[Event], int]:
        query = self.db.query(Event)

        if category_id:
            query = query.filter(Event.category_id == category_id)

        if city:
            like = f"%{city}%"
            query = query.join(Event.venue).filter(Event.venue.has(Venue.city.ilike(like)))

        if search:
            like = f"%{search}%"
            query = query.filter(or_(Event.title.ilike(like), Event.description.ilike(like)))

        total = query.count()

        sort_column = SORTABLE_FIELDS.get(sort_by, Event.created_at)
        sort_column = sort_column.asc() if order == "asc" else sort_column.desc()

        items = query.order_by(sort_column).offset(offset).limit(limit).all()
        return items, total
    

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
