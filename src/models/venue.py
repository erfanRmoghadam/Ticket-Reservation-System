from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship

from src.connections.database import Base


class Venue(Base):
    __tablename__ = "venues"

    venue_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False, index=True)
    total_capacity = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    seats = relationship("Seat", back_populates="venue")
    # events = relationship("Event", back_populates="venue")
