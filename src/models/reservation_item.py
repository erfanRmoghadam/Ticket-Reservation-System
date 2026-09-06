from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from src.connections.database import Base


class ReservationItem(Base):
    __tablename__ = "reservation_items"

    reservation_item_id = Column(Integer, primary_key=True, autoincrement=True)
    reservation_id = Column(Integer, ForeignKey("reservations.reservation_id"), nullable=False)
    session_seat_id = Column(Integer, ForeignKey("session_seats.session_seat_id"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    reservation = relationship("Reservation", back_populates="items")
    session_seat = relationship("SessionSeat", back_populates="reservation_items")
