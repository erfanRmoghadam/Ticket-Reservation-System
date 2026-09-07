from sqlalchemy.orm import Session

from src.models.reservation import Reservation
from src.models.reservation_item import ReservationItem
from src.models.session_seat import SessionSeat


class ReservationRepository:
    def __init__(self, db: Session):
        self.db = db

    def lock_session_seats(self, session_id: int, seat_ids: list[int]) -> list[SessionSeat]:
        """
        Locks the requested SessionSeat rows for the duration of the current
        transaction (SELECT ... FOR UPDATE).
        """
        return (
            self.db.query(SessionSeat)
            .filter(
                SessionSeat.session_id == session_id,
                SessionSeat.seat_id.in_(seat_ids),
            )
            .with_for_update()
            .all()
        )

    def create(self, reservation: Reservation) -> Reservation:
        self.db.add(reservation)
        self.db.flush()  #get reservation_id without committing yet
        return reservation

    def commit(self, reservation: Reservation) -> Reservation:
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def get_by_id(self, reservation_id: int) -> Reservation | None:
        return self.db.query(Reservation).filter(Reservation.reservation_id == reservation_id).first()

    def list_by_user(self, user_id: int) -> list[Reservation]:
        return (
            self.db.query(Reservation)
            .filter(Reservation.user_id == user_id)
            .order_by(Reservation.created_at.desc())
            .all()
        )

    def add_items(self, items: list[ReservationItem]) -> None:
        self.db.add_all(items)

    def save(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()
