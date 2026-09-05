from sqlalchemy.orm import Session

from src.models.venue import Venue


class VenueRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[Venue]:
        return self.db.query(Venue).order_by(Venue.name).all()

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
