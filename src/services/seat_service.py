from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.seat import Seat
from src.repository.seat_repository import SeatRepository
from src.repository.venue_repository import VenueRepository
from src.schemas.seat import BulkSeatCreateRequest, SeatUpdateRequest


class SeatService:
    def __init__(self, db: Session):
        self.repo = SeatRepository(db)
        self.venue_repo = VenueRepository(db)

    def bulk_create(self, venue_id: int, payload: BulkSeatCreateRequest) -> list[Seat]:
        if not self.venue_repo.get_venue_by_id(venue_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found.")
        seats = [
            Seat(venue_id=venue_id, row_label=s.row_label, seat_number=s.seat_number, seat_type=s.seat_type)
            for s in payload.seats
        ]
        return self.repo.bulk_create(seats)

    def get_by_id(self, seat_id: int) -> Seat:
        seat = self.repo.get_seat_by_id(seat_id)
        if not seat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seat not found.")
        return seat

    def update(self, seat_id: int, payload: SeatUpdateRequest) -> Seat:
        seat = self.get_by_id(seat_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(seat, key, value)
        return self.repo.update(seat)

    def delete(self, seat_id: int) -> None:
        seat = self.get_by_id(seat_id)
        self.repo.delete(seat)
