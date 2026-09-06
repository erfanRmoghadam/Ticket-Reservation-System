from sqlalchemy.orm import Session as DBSession

from src.models.event_session import EventSession
from src.models.session_seat import SessionSeat


class SessionRepository:
    def __init__(self, db: DBSession):
        self.db = db

    def list_by_event(self, event_id: int) -> list[EventSession]:
        return (
            self.db.query(EventSession)
            .filter(EventSession.event_id == event_id)
            .order_by(EventSession.start_time)
            .all()
        )

    def get_session_by_id(self, session_id: int) -> EventSession | None:
        return self.db.query(EventSession).filter(EventSession.session_id == session_id).first()

    def create(self, session: EventSession) -> EventSession:
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def update(self, session: EventSession) -> EventSession:
        self.db.commit()
        self.db.refresh(session)
        return session

    def delete(self, session: EventSession) -> None:
        self.db.delete(session)
        self.db.commit()

    def list_session_seats(self, session_id: int) -> list[SessionSeat]:
        return (
            self.db.query(SessionSeat)
            .filter(SessionSeat.session_id == session_id)
            .all()
        )

    def bulk_create_session_seats(self, session_seats: list[SessionSeat]) -> list[SessionSeat]:
        self.db.add_all(session_seats)
        self.db.commit()
        return session_seats
