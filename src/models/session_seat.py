from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from src.connections.database import Base


class SeatStatus:
    AVAILABLE = "available"
    RESERVED = "reserved"
    SOLD = "sold"


class SessionSeat(Base):
    __tablename__ = "session_seats"
    __table_args__ = (UniqueConstraint("session_id", "seat_id", name="unique_session_seat"),)

    session_seat_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("event_sessions.session_id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.seat_id"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default=SeatStatus.AVAILABLE)

    session = relationship("EventSession", back_populates="session_seats")
    seat = relationship("Seat", back_populates="session_seats")
    reservation_items = relationship("ReservationItem", back_populates="session_seat")
