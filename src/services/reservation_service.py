from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.config import settings
from src.models.reservation import Reservation, ReservationStatus
from src.models.reservation_item import ReservationItem
from src.models.session_seat import SessionSeat, SeatStatus
from src.models.user import User
from src.repository.reservation_repository import ReservationRepository
from src.repository.session_repository import SessionRepository
from src.schemas.reservation import ReservationCreateRequest
from src.connections.redis import get_redis


class ReservationService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ReservationRepository(db)
        self.session_repo = SessionRepository(db)
        self.redis = get_redis()

    def create(self, user: User, payload: ReservationCreateRequest) -> Reservation:
        if not payload.seat_ids:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="seat_ids cannot be empty.")

        event_session = self.session_repo.get_session_by_id(payload.session_id)
        if not event_session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")

        try:
            # *** important section: lock only the requested seat rows ***
            locked_seats: list[SessionSeat] = self.repo.lock_session_seats(
                payload.session_id, payload.seat_ids
            )

            if len(locked_seats) != len(set(payload.seat_ids)):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="One or more requested seats do not exist for this session.",
                )

            unavailable = [s for s in locked_seats if s.status != SeatStatus.AVAILABLE]
            if unavailable:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Seat(s) {[s.seat_id for s in unavailable]} are no longer available.",
                )

            total_price = sum(s.price for s in locked_seats)
            expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.RESERVATION_HOLD_MINUTES)

            reservation = Reservation(
                user_id=user.user_id,
                session_id=payload.session_id,
                status=ReservationStatus.PENDING,
                total_price=total_price,
                expires_at=expires_at,
            )
            reservation = self.repo.create(reservation)

            items = []
            for seat in locked_seats:
                seat.status = SeatStatus.RESERVED
                items.append(
                    ReservationItem(
                        reservation_id=reservation.reservation_id,
                        session_seat_id=seat.session_seat_id,
                        price=seat.price,
                    )
                )
            self.repo.add_items(items)
            self.repo.save()
            # *** end of impotant section: commit releases the row locks ***

        except HTTPException:
            self.repo.rollback()
            raise
        except Exception:
            self.repo.rollback()
            raise

        self.redis.delete(f"session:{payload.session_id}:seats")
        return self.repo.get_by_id(reservation.reservation_id)