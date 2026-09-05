from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.venue import Venue
from src.repository.venue_repository import VenueRepository
from src.schemas.venue import VenueCreateRequest, VenueUpdateRequest
from src.repository.seat_repository import SeatRepository


class VenueService:
    def __init__(self, db: Session):
        self.repo = VenueRepository(db)
        self.seat_repo = SeatRepository(db)

    def list_all(self) -> list[Venue]:
        return self.repo.list_all()

    def get_by_id(self, venue_id: int) -> Venue:
        venue = self.repo.get_venue_by_id(venue_id)
        if not venue:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found.")
        return venue

    def create(self, payload: VenueCreateRequest) -> Venue:
        venue = Venue(**payload.model_dump())
        return self.repo.create(venue)

    def update(self, venue_id: int, payload: VenueUpdateRequest) -> Venue:
        venue = self.get_by_id(venue_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(venue, key, value)
        return self.repo.update(venue)

    def delete(self, venue_id: int) -> None:
        venue = self.get_by_id(venue_id)
        self.repo.delete(venue)

    def list_seats(self, venue_id: int):
        self.get_by_id(venue_id) #404 if missing
        return self.seat_repo.list_by_venue(venue_id)
