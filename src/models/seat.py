from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from src.connections.database import Base


class SeatType:
    NORMAL = "normal"
    VIP = "vip"


class Seat(Base):
    __tablename__ = "seats"
    __table_args__ = (UniqueConstraint("venue_id", "row_label", "seat_number", name="unique_seat_position"),)

    seat_id = Column(Integer, primary_key=True, autoincrement=True)
    venue_id = Column(Integer, ForeignKey("venues.venue_id"), nullable=False)
    row_label = Column(String(10), nullable=False)
    seat_number = Column(Integer, nullable=False)
    seat_type = Column(String(20), default=SeatType.NORMAL)

    venue = relationship("Venue", back_populates="seats")
    # session_seats = relationship("SessionSeat", back_populates="seat")
