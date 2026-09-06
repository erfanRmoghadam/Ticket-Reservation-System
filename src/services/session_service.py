import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session as DBSession

from src.core.permissions import ensure_owner_or_admin
from src.models.event_session import EventSession
from src.models.session_seat import SessionSeat
from src.models.user import User
from src.repository.event_repository import EventRepository
from src.repository.seat_repository import SeatRepository
from src.repository.session_repository import SessionRepository
from src.schemas.session import SessionCreateRequest, SessionUpdateRequest



class SessionService:
    def __init__(self, db: DBSession):
        self.db = db
        self.repo = SessionRepository(db)
        self.event_repo = EventRepository(db)
        self.seat_repo = SeatRepository(db)

    def list_by_event(self, event_id: int) -> list[EventSession]:
        return self.repo.list_by_event(event_id)

    def get_by_id(self, session_id: int) -> EventSession:
        session = self.repo.get_session_by_id(session_id)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")
        return session

    def create(self, event_id: int, current_user: User, payload: SessionCreateRequest) -> EventSession:
        event = self.event_repo.get_event_by_id(event_id)
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found.")
        ensure_owner_or_admin(current_user, event.organizer_id)

        if payload.end_time <= payload.start_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="end_time must be after start_time."
            )

        session = EventSession(
            event_id=event_id,
            start_time=payload.start_time,
            end_time=payload.end_time,
        )
        session = self.repo.create(session)

        #seed SessionSeat rows from the venue's physical seat layout
        venue_seats = self.seat_repo.list_by_venue(event.venue_id)
        session_seats = [
            SessionSeat(session_id=session.session_id, seat_id=seat.seat_id, price=payload.default_price)
            for seat in venue_seats
        ]
        if session_seats:
            self.repo.bulk_create_session_seats(session_seats)

        return session

    def update(self, session_id: int, current_user: User, payload: SessionUpdateRequest) -> EventSession:
        session = self.get_by_id(session_id)
        event = self.event_repo.get_event_by_id(session.event_id)
        ensure_owner_or_admin(current_user, event.organizer_id)

        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(session, key, value)
        session = self.repo.update(session)
        return session

    def delete(self, session_id: int, current_user: User) -> None:
        session = self.get_by_id(session_id)
        event = self.event_repo.get_event_by_id(session.event_id)
        ensure_owner_or_admin(current_user, event.organizer_id)
        self.repo.delete(session)


