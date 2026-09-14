from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.models.venue import Venue


class VenueRepository:
    def __init__(self, db: Session):
        self.db = db

    def search(
        self,
        city: str | None = None,
        search: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Venue], int]:
        query = self.db.query(Venue)
        if city:
            like = f"%{city}%"
            query = query.filter(Venue.city.ilike(like))
        if search:
            like = f"%{search}%"
            query = query.filter(or_(Venue.name.ilike(like), Venue.address.ilike(like)))

        total = query.count()
        items = query.order_by(Venue.name).offset(offset).limit(limit).all()
        return items, total
      

    def get_venue_by_id(self, venue_id: int) -> Venue | None:
        return self.db.query(Venue).filter(Venue.venue_id == venue_id).first()

    def create(self, venue: Venue) -> Venue:
        self.db.add(venue)
        self.db.commit()
        self.db.refresh(venue)
        return venue

    def update(self, venue: Venue) -> Venue:
        self.db.commit()
        self.db.refresh(venue)
        return venue

    def delete(self, venue: Venue) -> None:
        self.db.delete(venue)
        self.db.commit()
