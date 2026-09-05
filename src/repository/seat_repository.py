from sqlalchemy.orm import Session

from src.models.seat import Seat


class SeatRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_venue(self, venue_id: int) -> list[Seat]:
        return (
            self.db.query(Seat)
            .filter(Seat.venue_id == venue_id)
            .order_by(Seat.row_label, Seat.seat_number)
            .all()
        )

    def get_seat_by_id(self, seat_id: int) -> Seat | None:
        return self.db.query(Seat).filter(Seat.seat_id == seat_id).first()

    def bulk_create(self, seats: list[Seat]) -> list[Seat]:
        self.db.add_all(seats)
        self.db.commit()
        for seat in seats:
            self.db.refresh(seat)
        return seats

    def update(self, seat: Seat) -> Seat:
        self.db.commit()
        self.db.refresh(seat)
        return seat

    def delete(self, seat: Seat) -> None:
        self.db.delete(seat)
        self.db.commit()
