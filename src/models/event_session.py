from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from src.connections.database import Base


class SessionStatus:
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class EventSession(Base):
    __tablename__ = "event_sessions"

    session_id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("events.event_id"), nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    status = Column(String(20), default=SessionStatus.SCHEDULED)

    event = relationship("Event", back_populates="sessions")
    session_seats = relationship("SessionSeat", back_populates="session", cascade="all, delete-orphan")
    # reservations = relationship("Reservation", back_populates="session")
